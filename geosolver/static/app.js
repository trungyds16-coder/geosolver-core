// ==========================================================================
// GEOMETRY ENGINE & INTERACTIVE CANVAS (OXY + OLYMPIC)
// ==========================================================================

const canvas = document.getElementById("geoCanvas");
const ctx = canvas.getContext("2d");
const statusBar = document.getElementById("status-bar");
const jsonDisplay = document.getElementById("json-ast-display");
const solutionOutput = document.getElementById("solution-output");
const distPaEl = document.getElementById("dist-pa");
const distPmEl = document.getElementById("dist-pm");

// Coordinate transformation:
// World coordinates: Cartesian Oxy (units in math plane)
// Screen coordinates: pixels on canvas
let view = {
    originX: 0,
    originY: 0,
    scale: 45, // pixels per math unit
    isPanning: false,
    panStartX: 0,
    panStartY: 0
};

// Current active tool
let currentTool = "select";
let selectedPoint = null;
let hoveredPoint = null;
let hoveredEntity = null;
let constructionStep = 0;
let tempPoints = [];

// Data structures
let points = [];       // { id, name, x, y, color, fixed, onCircle, parentCircle }
let segments = [];     // { p1, p2, color, style, label }
let lines = [];        // { p1, p2, color, style, label }
let circles = [];      // { id, center, r, p1, p2, color, label }
let constraints = [];  // { type, desc, data }
let equalAngleArcs = []; // arcs to highlight angle chasing

// Resize canvas
function resizeCanvas() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
    if (view.originX === 0 && view.originY === 0) {
        // Center Oxy
        view.originX = canvas.width / 2 - 40;
        view.originY = canvas.height / 2 + 60;
    }
    redraw();
}
window.addEventListener("resize", resizeCanvas);

// Coordinate transforms
function toScreen(x, y) {
    return {
        px: view.originX + x * view.scale,
        py: view.originY - y * view.scale
    };
}

function toWorld(px, py) {
    return {
        x: (px - view.originX) / view.scale,
        y: -(py - view.originY) / view.scale
    };
}

// ==========================================================================
// TOOLBAR SWITCHING
// ==========================================================================
document.querySelectorAll(".tool-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        document.querySelectorAll(".tool-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        currentTool = btn.dataset.tool;
        constructionStep = 0;
        tempPoints = [];
        updateStatus();
    });
});

// TABS SWITCHING
document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
        document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
        btn.classList.add("active");
        document.getElementById(btn.dataset.tab).classList.add("active");
    });
});

function updateStatus() {
    const msgs = {
        "select": "Chế độ Chọn & Kéo: Nhấp chuột giữ điểm tự do (ví dụ điểm A) để kéo và xem hình động biến thiên.",
        "point": "Chế độ Điểm: Nhấp chuột trên mặt phẳng để đặt một điểm mới.",
        "segment": "Chế độ Đoạn Thẳng: Nhấp vào 2 điểm để tạo đoạn thẳng.",
        "line": "Chế độ Đường Thẳng: Nhấp vào 2 điểm để kéo dài đường thẳng vô tận.",
        "circle": "Chế độ Đường Tròn: Nhấp điểm thứ 1 làm tâm, nhấp điểm thứ 2 để xác định bán kính.",
        "square": "Chế độ Hình Vuông: Nhấp 2 điểm làm 1 cạnh, hệ thống sẽ tự động dựng hình vuông hoàn chỉnh.",
        "tangent": "Chế độ Tiếp Tuyến: Nhấp chọn một điểm và chọn một đường tròn để kẻ 2 tiếp tuyến.",
        "perpendicular": "Chế độ Vuông Góc: Nhấp 1 điểm và 1 đường thẳng để hạ đường vuông góc & lấy hình chiếu.",
        "angle-line": "Chế độ Góc: Nhấp 1 điểm để dựng đường thẳng tạo góc cố định."
    };
    statusBar.innerHTML = msgs[currentTool] || "Sẵn sàng.";
}

// ==========================================================================
// MATH HELPER FUNCTIONS
// ==========================================================================
function dist(p1, p2) {
    return Math.hypot(p1.x - p2.x, p1.y - p2.y);
}

function projectPointToLine(P, A, B) {
    const dx = B.x - A.x;
    const dy = B.y - A.y;
    const lenSq = dx * dx + dy * dy;
    if (lenSq === 0) return { x: A.x, y: A.y };
    const t = ((P.x - A.x) * dx + (P.y - A.y) * dy) / lenSq;
    return {
        x: A.x + t * dx,
        y: A.y + t * dy
    };
}

function intersectLines(A, B, C, D) {
    // Line AB: a1 x + b1 y = c1
    const a1 = B.y - A.y;
    const b1 = A.x - B.x;
    const c1 = a1 * A.x + b1 * A.y;

    // Line CD: a2 x + b2 y = c2
    const a2 = D.y - C.y;
    const b2 = C.x - D.x;
    const c2 = a2 * C.x + b2 * C.y;

    const det = a1 * b2 - a2 * b1;
    if (Math.abs(det) < 1e-9) return null; // parallel
    return {
        x: (c1 * b2 - c2 * b1) / det,
        y: (a1 * c2 - a2 * c1) / det
    };
}

// Find nearby point for snapping
function findNearbyPoint(worldPos, maxPixelDist = 12) {
    for (let p of points) {
        const sP = toScreen(p.x, p.y);
        const sM = toScreen(worldPos.x, worldPos.y);
        if (Math.hypot(sP.px - sM.px, sP.py - sM.py) <= maxPixelDist) {
            return p;
        }
    }
    return null;
}

// ==========================================================================
// NẠP BÀI TOÁN MẪU: CÂU VIII (ĐỀ THI OXY TRONG ẢNH)
// ==========================================================================
let isDemoCauVIII = false;

function loadDemoCauVIII() {
    isDemoCauVIII = true;
    points = [];
    segments = [];
    lines = [];
    circles = [];
    constraints = [];
    equalAngleArcs = [];

    // Tọa độ chuẩn của bài toán
    // B(-1, 4), D(5, 0), BD là đường kính
    // Tâm O của BD: O(( -1 + 5)/2, (4 + 0)/2) = (2, 2)
    // Bán kính R = sqrt((5-2)^2 + (0-2)^2) = sqrt(9 + 4) = sqrt(13) ~ 3.6055
    const B = { id: "B", name: "B", x: -1, y: 4, color: "#38bdf8", fixed: true };
    const D = { id: "D", name: "D", x: 5, y: 0, color: "#94a3b8", fixed: true };
    const O = { id: "O", name: "O", x: 2, y: 2, color: "#64748b", fixed: true };
    const R = Math.hypot(D.x - O.x, D.y - O.y);

    // C(5, 4) nằm trên đường tròn (vì (5-2)^2 + (4-2)^2 = 13 = R^2)
    const C = { id: "C", name: "C", x: 5, y: 4, color: "#94a3b8", fixed: true };

    // A ban đầu ở (0, -1) nằm trên đường tròn
    // Người dùng CÓ THỂ KÉO THẢ điểm A trên đường tròn!
    const A = { id: "A", name: "A", x: 0, y: -1, color: "#f43f5e", fixed: false, onCircle: "circle_BD" };

    points.push(B, D, O, C, A);

    // Đường tròn đường kính BD
    circles.push({
        id: "circle_BD",
        center: O,
        r: R,
        color: "rgba(59, 130, 246, 0.4)",
        label: "(O) đường kính BD"
    });

    // Đường thẳng BC (y = 4)
    lines.push({ p1: B, p2: C, color: "rgba(148, 163, 184, 0.5)", style: "solid", label: "BC" });
    // Đường thẳng BD
    lines.push({ p1: B, p2: D, color: "rgba(148, 163, 184, 0.5)", style: "solid", label: "BD" });

    // Cập nhật các điểm phụ thuộc M, N, P dựa trên vị trí A
    updateDependentPoints();

    // Căn góc camera nhìn rõ toàn bộ hình
    view.scale = 55;
    view.originX = canvas.width / 2 - 100;
    view.originY = canvas.height / 2 + 50;

    syncConstraintAST();
    redraw();
    statusBar.innerHTML = "✅ Đã nạp bài mẫu Câu VIII! Hãy thử <b>kéo thả đỉnh A</b> trên đường tròn để thấy <b>PA = PM luôn bằng nhau</b>.";
}

// Tự động tính toán M, N, P khi A di chuyển
function updateDependentPoints() {
    if (!isDemoCauVIII) return;

    const A = points.find(p => p.id === "A");
    const B = points.find(p => p.id === "B");
    const C = points.find(p => p.id === "C");
    const D = points.find(p => p.id === "D");
    if (!A || !B || !C || !D) return;

    // 1. M là hình chiếu của A trên BC (line BC qua B và C)
    const M_pos = projectPointToLine(A, B, C);
    let M = points.find(p => p.id === "M");
    if (!M) {
        M = { id: "M", name: "M", x: M_pos.x, y: M_pos.y, color: "#10b981", fixed: true };
        points.push(M);
    } else {
        M.x = M_pos.x;
        M.y = M_pos.y;
    }

    // 2. N là hình chiếu của A trên BD (line BD qua B và D)
    const N_pos = projectPointToLine(A, B, D);
    let N = points.find(p => p.id === "N");
    if (!N) {
        N = { id: "N", name: "N", x: N_pos.x, y: N_pos.y, color: "#10b981", fixed: true };
        points.push(N);
    } else {
        N.x = N_pos.x;
        N.y = N_pos.y;
    }

    // 3. P là giao điểm của MN và AC
    const P_pos = intersectLines(M, N, A, C);
    let P = points.find(p => p.id === "P");
    if (P_pos) {
        if (!P) {
            P = { id: "P", name: "P", x: P_pos.x, y: P_pos.y, color: "#f59e0b", fixed: true };
            points.push(P);
        } else {
            P.x = P_pos.x;
            P.y = P_pos.y;
        }
    }

    // Cập nhật các đoạn nối & màu sắc
    segments = [
        { p1: B, p2: C, color: "#64748b", style: "solid" },
        { p1: C, p2: D, color: "#64748b", style: "solid" },
        { p1: D, p2: A, color: "#64748b", style: "solid" },
        { p1: A, p2: B, color: "#38bdf8", style: "solid" },
        { p1: B, p2: D, color: "#475569", style: "dashed" },
        { p1: A, p2: C, color: "#a855f7", style: "solid", label: "AC (x - y - 1 = 0)" },
        { p1: A, p2: M, color: "#10b981", style: "dashed", label: "AM ⊥ BC" },
        { p1: A, p2: N, color: "#10b981", style: "dashed", label: "AN ⊥ BD" },
        { p1: M, p2: N, color: "#f59e0b", style: "solid", label: "MN" }
    ];

    if (P) {
        segments.push(
            { p1: P, p2: A, color: "#ef4444", style: "bold", label: "PA" },
            { p1: P, p2: M, color: "#ef4444", style: "bold", label: "PM" }
        );

        // Đo khoảng cách thời gian thực
        const dPA = dist(P, A);
        const dPM = dist(P, M);
        distPaEl.textContent = dPA.toFixed(3);
        distPmEl.textContent = dPM.toFixed(3);
        document.getElementById("verdict-isosceles").innerHTML = 
            `Kiểm chứng bất biến: <b>PA (${dPA.toFixed(3)}) = PM (${dPM.toFixed(3)})</b> $\\implies \\Delta PAM$ luôn cân tại P!`;
    }

    // Góc bằng nhau (Angle Chasing)
    equalAngleArcs = [
        { vertex: M, p1: A, p2: N, label: "∠AMN", color: "#f59e0b" },
        { vertex: B, p1: A, p2: D, label: "∠ABD", color: "#f59e0b" },
        { vertex: C, p1: A, p2: D, label: "∠ACD", color: "#f59e0b" },
        { vertex: A, p1: M, p2: C, label: "∠MAC", color: "#f59e0b" }
    ];
}

// Đồng bộ cây cú pháp ràng buộc dạng JSON
function syncConstraintAST() {
    const ast = {
        meta: {
            problem: isDemoCauVIII ? "Câu VIII - Đề thi Tuyển sinh Oxy" : "Mô hình Dựng hình Tự do",
            version: "2.0-hybrid"
        },
        entities: {
            points: points.map(p => ({ id: p.id || p.name, name: p.name, coords: [+(p.x.toFixed(2)), +(p.y.toFixed(2))], fixed: !!p.fixed })),
            circles: circles.map(c => ({ id: c.id, center: c.center.name, radius: +(c.r.toFixed(2)) }))
        },
        constraints: [
            ...(isDemoCauVIII ? [
                { type: "CONCYCLIC_DIAMETER", points: ["A", "B", "C", "D"], diameter: ["B", "D"] },
                { type: "PERPENDICULAR_PROJECTION", from: "A", to_line: ["B", "C"], result: "M" },
                { type: "PERPENDICULAR_PROJECTION", from: "A", to_line: ["B", "D"], result: "N" },
                { type: "LINE_INTERSECTION", line1: ["M", "N"], line2: ["A", "C"], result: "P" },
                { type: "INVARIANT_DETECTED", property: "ISOSCELES_TRIANGLE", triangle: "PAM", apex: "P", equality: "PA == PM" }
            ] : constraints)
        ]
    };
    jsonDisplay.textContent = JSON.stringify(ast, null, 2);
}

// ==========================================================================
// THAO TÁC CHUỘT TRÊN CANVAS (MOUSE EVENTS)
// ==========================================================================
canvas.addEventListener("mousedown", (e) => {
    const rect = canvas.getBoundingClientRect();
    const mousePx = e.clientX - rect.left;
    const mousePy = e.clientY - rect.top;
    const wPos = toWorld(mousePx, mousePy);

    if (e.button === 2) { // Right click -> Pan
        view.isPanning = true;
        view.panStartX = mousePx - view.originX;
        view.panStartY = mousePy - view.originY;
        return;
    }

    const clickedPoint = findNearbyPoint(wPos);

    if (currentTool === "select") {
        if (clickedPoint && !clickedPoint.fixed) {
            selectedPoint = clickedPoint;
        }
    } else if (currentTool === "point") {
        const snap = document.getElementById("chk-snap").checked;
        const x = snap ? Math.round(wPos.x * 2) / 2 : wPos.x;
        const y = snap ? Math.round(wPos.y * 2) / 2 : wPos.y;
        const name = String.fromCharCode(65 + (points.length % 26));
        points.push({ id: name, name: name, x, y, color: "#38bdf8", fixed: false });
        syncConstraintAST();
        redraw();
    } else if (currentTool === "segment" || currentTool === "line") {
        if (clickedPoint) {
            tempPoints.push(clickedPoint);
            if (tempPoints.length === 2) {
                if (currentTool === "segment") {
                    segments.push({ p1: tempPoints[0], p2: tempPoints[1], color: "#e2e8f0", style: "solid" });
                } else {
                    lines.push({ p1: tempPoints[0], p2: tempPoints[1], color: "#94a3b8", style: "solid" });
                }
                tempPoints = [];
                syncConstraintAST();
                redraw();
            }
        }
    } else if (currentTool === "circle") {
        if (clickedPoint) {
            tempPoints.push(clickedPoint);
            if (tempPoints.length === 2) {
                const r = dist(tempPoints[0], tempPoints[1]);
                circles.push({
                    id: "C_" + tempPoints[0].name,
                    center: tempPoints[0],
                    r: r,
                    color: "rgba(59, 130, 246, 0.4)",
                    label: `C(${tempPoints[0].name})`
                });
                tempPoints = [];
                syncConstraintAST();
                redraw();
            }
        }
    } else if (currentTool === "square") {
        // VẼ HÌNH VUÔNG TỰ ĐỘNG KHI CHỌN 2 ĐỈNH
        if (clickedPoint) {
            tempPoints.push(clickedPoint);
            if (tempPoints.length === 2) {
                const p1 = tempPoints[0];
                const p2 = tempPoints[1];
                // Vector p1 -> p2: (dx, dy)
                const dx = p2.x - p1.x;
                const dy = p2.y - p1.y;
                // Quay 90 độ ngược chiều kim đồng hồ: (-dy, dx)
                const p3 = { id: p2.name + "_sq", name: p2.name + "'", x: p2.x - dy, y: p2.y + dx, color: "#fbbf24", fixed: false };
                const p4 = { id: p1.name + "_sq", name: p1.name + "'", x: p1.x - dy, y: p1.y + dx, color: "#fbbf24", fixed: false };
                points.push(p3, p4);
                segments.push(
                    { p1: p1, p2: p2, color: "#f59e0b", style: "solid" },
                    { p1: p2, p2: p3, color: "#f59e0b", style: "solid" },
                    { p1: p3, p2: p4, color: "#f59e0b", style: "solid" },
                    { p1: p4, p2: p1, color: "#f59e0b", style: "solid" }
                );
                tempPoints = [];
                syncConstraintAST();
                redraw();
                statusBar.innerHTML = "✅ Đã dựng hình vuông hoàn chỉnh từ 2 đỉnh chọn!";
            }
        }
    } else if (currentTool === "tangent") {
        // DỰNG TIẾP TUYẾN TỪ 1 ĐIỂM ĐẾN ĐƯỜNG TRÒN
        if (clickedPoint) {
            tempPoints.push(clickedPoint);
        } else if (tempPoints.length === 1 && circles.length > 0) {
            // Click chọn đường tròn
            const c = circles[0]; // Chọn đường tròn đầu tiên nếu có
            const P = tempPoints[0];
            const d = dist(P, c.center);
            if (d >= c.r) {
                const angle = Math.atan2(P.y - c.center.y, P.x - c.center.x);
                const alpha = Math.acos(c.r / d);
                // Hai tiếp điểm
                const t1 = {
                    id: "T1", name: "T₁",
                    x: c.center.x + c.r * Math.cos(angle + alpha),
                    y: c.center.y + c.r * Math.sin(angle + alpha),
                    color: "#a855f7", fixed: true
                };
                const t2 = {
                    id: "T2", name: "T₂",
                    x: c.center.x + c.r * Math.cos(angle - alpha),
                    y: c.center.y + c.r * Math.sin(angle - alpha),
                    color: "#a855f7", fixed: true
                };
                points.push(t1, t2);
                lines.push(
                    { p1: P, p2: t1, color: "#c084fc", style: "solid", label: "Tiếp tuyến 1" },
                    { p1: P, p2: t2, color: "#c084fc", style: "solid", label: "Tiếp tuyến 2" }
                );
                tempPoints = [];
                syncConstraintAST();
                redraw();
                statusBar.innerHTML = "✅ Đã kẻ 2 tiếp tuyến chuẩn xác từ điểm đến đường tròn!";
            } else {
                statusBar.innerHTML = "⚠️ Điểm nằm bên trong đường tròn, không có tiếp tuyến!";
                tempPoints = [];
            }
        }
    } else if (currentTool === "angle-line") {
        if (clickedPoint) {
            tempPoints = [clickedPoint];
            document.getElementById("angle-modal").classList.add("active");
        }
    }
});

// Canvas Context Menu (chặn chuột phải)
canvas.addEventListener("contextmenu", e => e.preventDefault());

canvas.addEventListener("mousemove", (e) => {
    const rect = canvas.getBoundingClientRect();
    const mousePx = e.clientX - rect.left;
    const mousePy = e.clientY - rect.top;
    const wPos = toWorld(mousePx, mousePy);

    if (view.isPanning) {
        view.originX = mousePx - view.panStartX;
        view.originY = mousePy - view.panStartY;
        redraw();
        return;
    }

    if (selectedPoint) {
        if (selectedPoint.onCircle) {
            // Ràng buộc di chuyển trên đường tròn
            const circle = circles.find(c => c.id === selectedPoint.onCircle);
            if (circle) {
                const angle = Math.atan2(wPos.y - circle.center.y, wPos.x - circle.center.x);
                selectedPoint.x = circle.center.x + circle.r * Math.cos(angle);
                selectedPoint.y = circle.center.y + circle.r * Math.sin(angle);
            }
        } else {
            selectedPoint.x = wPos.x;
            selectedPoint.y = wPos.y;
        }

        if (isDemoCauVIII) {
            updateDependentPoints();
        }
        syncConstraintAST();
        redraw();
        return;
    }

    // Hover detection
    hoveredPoint = findNearbyPoint(wPos);
    canvas.style.cursor = hoveredPoint ? "pointer" : (currentTool === "select" ? "default" : "crosshair");
    redraw();
});

window.addEventListener("mouseup", () => {
    selectedPoint = null;
    view.isPanning = false;
});

// Zoom
canvas.addEventListener("wheel", (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.1 : 0.9;
    const rect = canvas.getBoundingClientRect();
    const mousePx = e.clientX - rect.left;
    const mousePy = e.clientY - rect.top;

    // Zoom centered on mouse
    view.originX = mousePx - (mousePx - view.originX) * zoomFactor;
    view.originY = mousePy - (mousePy - view.originY) * zoomFactor;
    view.scale *= zoomFactor;
    redraw();
});

// Modal Đặt Góc
document.getElementById("btn-confirm-angle").addEventListener("click", () => {
    const deg = parseFloat(document.getElementById("input-angle-val").value) || 0;
    document.getElementById("angle-modal").classList.remove("active");
    if (tempPoints.length === 1) {
        const p1 = tempPoints[0];
        const rad = (deg * Math.PI) / 180;
        const p2 = {
            id: p1.name + "_" + deg,
            name: `${p1.name}(${deg}°)`,
            x: p1.x + 3 * Math.cos(rad),
            y: p1.y + 3 * Math.sin(rad),
            color: "#38bdf8",
            fixed: false
        };
        points.push(p2);
        lines.push({ p1: p1, p2: p2, color: "#38bdf8", style: "solid", label: `${deg}°` });
        tempPoints = [];
        syncConstraintAST();
        redraw();
    }
});
document.getElementById("btn-cancel-angle").addEventListener("click", () => {
    document.getElementById("angle-modal").classList.remove("active");
    tempPoints = [];
});

// Nạp Demo
document.getElementById("btn-load-demo").addEventListener("click", loadDemoCauVIII);
document.getElementById("btn-clear").addEventListener("click", () => {
    points = [];
    segments = [];
    lines = [];
    circles = [];
    constraints = [];
    equalAngleArcs = [];
    isDemoCauVIII = false;
    distPaEl.textContent = "--";
    distPmEl.textContent = "--";
    syncConstraintAST();
    redraw();
    statusBar.innerHTML = "Bảng vẽ đã được xóa sạch.";
});

// ==========================================================================
// RENDER & DRAWING LOOP
// ==========================================================================
function redraw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Lưới Oxy
    if (document.getElementById("chk-grid").checked) {
        drawGrid();
    }

    // 2. Đường tròn
    circles.forEach(c => {
        const sC = toScreen(c.center.x, c.center.y);
        const sR = c.r * view.scale;
        ctx.beginPath();
        ctx.arc(sC.px, sC.py, sR, 0, Math.PI * 2);
        ctx.strokeStyle = c.color;
        ctx.lineWidth = 1.8;
        ctx.stroke();

        if (c.label) {
            ctx.fillStyle = "#94a3b8";
            ctx.font = "11px monospace";
            ctx.fillText(c.label, sC.px - sR * 0.7, sC.py - sR * 0.7);
        }
    });

    // 3. Đường thẳng (kéo dài)
    lines.forEach(l => {
        const s1 = toScreen(l.p1.x, l.p1.y);
        const s2 = toScreen(l.p2.x, l.p2.y);
        const dx = s2.px - s1.px;
        const dy = s2.py - s1.py;
        const len = Math.hypot(dx, dy);
        if (len > 0) {
            ctx.beginPath();
            ctx.moveTo(s1.px - dx * 20, s1.py - dy * 20);
            ctx.lineTo(s2.px + dx * 20, s2.py + dy * 20);
            ctx.strokeStyle = l.color;
            ctx.lineWidth = 1.5;
            ctx.stroke();
        }
    });

    // 4. Đoạn thẳng
    segments.forEach(s => {
        const s1 = toScreen(s.p1.x, s.p1.y);
        const s2 = toScreen(s.p2.x, s.p2.y);
        ctx.beginPath();
        ctx.moveTo(s1.px, s1.py);
        ctx.lineTo(s2.px, s2.py);
        ctx.strokeStyle = s.color;
        ctx.lineWidth = s.style === "bold" ? 3 : 1.6;
        if (s.style === "dashed") ctx.setLineDash([5, 4]);
        else ctx.setLineDash([]);
        ctx.stroke();
        ctx.setLineDash([]);

        // Label
        if (s.label) {
            const midX = (s1.px + s2.px) / 2;
            const midY = (s1.py + s2.py) / 2;
            ctx.fillStyle = s.color;
            ctx.font = "11px sans-serif";
            ctx.fillText(s.label, midX + 6, midY - 6);
        }
    });

    // 5. Cung góc bằng nhau (Angle Chasing Visualization)
    if (document.getElementById("chk-angles").checked) {
        equalAngleArcs.forEach(arc => {
            const v = toScreen(arc.vertex.x, arc.vertex.y);
            const a1 = Math.atan2(view.originY - arc.p1.y * view.scale - v.py, toScreen(arc.p1.x, arc.p1.y).px - v.px);
            const a2 = Math.atan2(view.originY - arc.p2.y * view.scale - v.py, toScreen(arc.p2.x, arc.p2.y).px - v.px);
            
            ctx.beginPath();
            ctx.arc(v.px, v.py, 18, a1, a2);
            ctx.strokeStyle = arc.color;
            ctx.lineWidth = 2;
            ctx.stroke();
        });
    }

    // 6. Điểm
    points.forEach(p => {
        const s = toScreen(p.x, p.y);
        const isHover = (hoveredPoint && hoveredPoint.id === p.id);
        const isSel = (selectedPoint && selectedPoint.id === p.id);

        ctx.beginPath();
        ctx.arc(s.px, s.py, isHover || isSel ? 7 : 5, 0, Math.PI * 2);
        ctx.fillStyle = p.color || "#38bdf8";
        ctx.fill();
        ctx.strokeStyle = isHover || isSel ? "#ffffff" : "#0f172a";
        ctx.lineWidth = 2;
        ctx.stroke();

        // Tên điểm & Tọa độ
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 13px sans-serif";
        ctx.fillText(`${p.name} (${p.x.toFixed(1)}, ${p.y.toFixed(1)})`, s.px + 9, s.py - 9);
    });
}

function drawGrid() {
    ctx.strokeStyle = "rgba(51, 65, 85, 0.4)";
    ctx.lineWidth = 1;

    const startW = toWorld(0, canvas.height);
    const endW = toWorld(canvas.width, 0);

    const minX = Math.floor(startW.x) - 1;
    const maxX = Math.ceil(endW.x) + 1;
    const minY = Math.floor(startW.y) - 1;
    const maxY = Math.ceil(endW.y) + 1;

    // Grid dọc
    for (let x = minX; x <= maxX; x++) {
        const px = view.originX + x * view.scale;
        ctx.beginPath();
        ctx.moveTo(px, 0);
        ctx.lineTo(px, canvas.height);
        ctx.stroke();
    }

    // Grid ngang
    for (let y = minY; y <= maxY; y++) {
        const py = view.originY - y * view.scale;
        ctx.beginPath();
        ctx.moveTo(0, py);
        ctx.lineTo(canvas.width, py);
        ctx.stroke();
    }

    // Trục chính Oxy
    ctx.strokeStyle = "rgba(148, 163, 184, 0.7)";
    ctx.lineWidth = 2;

    // Ox
    ctx.beginPath();
    ctx.moveTo(0, view.originY);
    ctx.lineTo(canvas.width, view.originY);
    ctx.stroke();

    // Oy
    ctx.beginPath();
    ctx.moveTo(view.originX, 0);
    ctx.lineTo(view.originX, canvas.height);
    ctx.stroke();

    // Nhãn trục
    ctx.fillStyle = "#94a3b8";
    ctx.font = "12px monospace";
    ctx.fillText("O", view.originX - 14, view.originY + 16);
    ctx.fillText("x", canvas.width - 16, view.originY - 8);
    ctx.fillText("y", view.originX + 8, 18);
}

// ==========================================================================
// KẾT NỐI SOLVER API
// ==========================================================================
document.getElementById("btn-run-solver").addEventListener("click", async () => {
    solutionOutput.innerHTML = `<div class="empty-state">⏳ Đang chạy bộ suy luận hình học và bộ giải đại số SymPy...</div>`;

    try {
        const res = await fetch("/api/solve_cau_viii", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({})
        });
        const data = await res.json();

        if (data.success) {
            let html = "";
            data.result.steps.forEach((step, idx) => {
                html += `
                    <div class="solution-step-card">
                        <div class="step-title">Bước ${idx + 1}: ${step.stage}</div>
                        <div class="step-detail">${step.detail}</div>
                    </div>
                `;
            });
            html += `
                <div class="solution-step-card" style="border-left-color: #10b981; background: rgba(16, 185, 129, 0.1);">
                    <div class="step-title" style="color: #34d399;">🎯 ĐÁP SỐ CHÍNH XÁC</div>
                    <div class="step-detail">
                        • Điểm <b>P</b>: <code>(${data.result.P[0]}, ${data.result.P[1]})</code> = <b>P(5/2; 3/2)</b><br>
                        • Điểm <b>A</b>: <code>(${data.result.A[0]}, ${data.result.A[1]})</code> = <b>A(0; -1)</b><br>
                        • Điểm <b>B</b>: <code>(${data.result.B[0]}, ${data.result.B[1]})</code> = <b>B(-1; 4)</b>
                    </div>
                </div>
            `;
            solutionOutput.innerHTML = html;

            // Render KaTeX math
            if (window.renderMathInElement) {
                renderMathInElement(solutionOutput, {
                    delimiters: [
                        { left: "$$", right: "$$", display: true },
                        { left: "$", right: "$", display: false }
                    ]
                });
            }
        } else {
            solutionOutput.innerHTML = `<div class="empty-state" style="color: #ef4444;">Lỗi solver: ${data.error}</div>`;
        }
    } catch (err) {
        solutionOutput.innerHTML = `<div class="empty-state" style="color: #ef4444;">Không thể kết nối đến server backend Python: ${err}</div>`;
    }
});

// Khởi tạo
resizeCanvas();
loadDemoCauVIII();
