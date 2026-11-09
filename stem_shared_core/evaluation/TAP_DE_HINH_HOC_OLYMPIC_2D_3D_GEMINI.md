# ĐẠI TUYỂN TẬP BÀI TOÁN HÌNH HỌC KINH ĐIỂN 2D & 3D (SHARYGIN, IMO SHORTLIST, HÌNH KHÔNG GIAN THPT)
Nguồn dữ liệu gốc: `D:\AI DATA\toan hinh`.
Dành cho: Hội đồng Thẩm định Sư phạm & Lời giải Logic Gemini (Google AI Studio).

===========================================================================

## NGUỒN: ABEAUTIFULJOURNEYTHROUGHOLYMPIADGEOMETRY_0A4D64B68D
- **Phân hệ:** [HÌNH HỌC PHẲNG OLYMPIC 2D]
- **Tên file:** `ABeautifulJourneyThroughOlympiadGeometry_0a4d64b68d.pdf` (146 trang)

### [Trang 4 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Version 1.0.0
www.olympiadgeometry.com
Cover created by Damjan Lozanovski
All illustrations created with GeoGebra (www.geogebra.org)
Copyright c⃝2016 by Stefan Lozanovski
All rights reserved. No part of this book may be reproduced, distributed, or
transmitted in any form or by any means, including photocopying, recording,
or other electronic or mechanical methods, without the prior written permission
of the author.

### [Trang 5 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Contents
Introduction
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
v
I
Lessons
1
Congruence of Triangles . . . . . . . . . . . . . . . . . . . . . . . .
2
Angles of a Transversal
. . . . . . . . . . . . . . . . . . . . . . . .
3
Area of Plane Figures
. . . . . . . . . . . . . . . . . . . . . . . . .
3.1
Area of Triangles . . . . . . . . . . . . . . . . . . . . . . . . . . .
4
Similarity of Triangles . . . . . . . . . . . . . . . . . . . . . . . . .
5
Circles . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
5.1
Symmetry in a Circle . . . . . . . . . . . . . . . . . . . . . . . . .
5.2
Angles in a Circle . . . . . . . . . . . . . . . . . . . . . . . . . . .
6
A Few Important Centers in a Triangle . . . . . . . . . . . . . .
7
Excircles . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
A Few Useful Lemmas . . . . . . . . . . . . . . . . . . . . . . . . .
8.1
Butterﬂy Theorem . . . . . . . . . . . . . . . . . . . . . . . . . .
8.2
Miquel’s Theorem
. . . . . . . . . . . . . . . . . . . . . . . . . .
8.3
Tangent Segments
. . . . . . . . . . . . . . . . . . . . . . . . . .
8.4
Simson Line Theorem
. . . . . . . . . . . . . . . . . . . . . . . .
8.5
Euler Line . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8.6
Nine Point Circle . . . . . . . . . . . . . . . . . . . . . . . . . . .
8.7
Eight Point Circle
. . . . . . . . . . . . . . . . . . . . . . . . . .
9
Basic Trigonometry . . . . . . . . . . . . . . . . . . . . . . . . . . .
10 Power of a Point . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
10.1 Radical axis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
10.2 Radical center . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
11 Collinearity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
11.1 Manual Approach . . . . . . . . . . . . . . . . . . . . . . . . . . .
11.2 Radical Axis
. . . . . . . . . . . . . . . . . . . . . . . . . . . . .
11.3 Menelaus’ Theorem . . . . . . . . . . . . . . . . . . . . . . . . . .
i

### [Trang 6 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Stefan Lozanovski
11.4 Pascal’s Theorem . . . . . . . . . . . . . . . . . . . . . . . . . . .
11.5 Desargues’ Theorem . . . . . . . . . . . . . . . . . . . . . . . . .
12 Concurrence
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
12.1 Manual Approach . . . . . . . . . . . . . . . . . . . . . . . . . . .
12.2 Special Lines
. . . . . . . . . . . . . . . . . . . . . . . . . . . . .
12.3 Special Point . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
12.4 Radical Center . . . . . . . . . . . . . . . . . . . . . . . . . . . .
12.5 Ceva’s Theorem . . . . . . . . . . . . . . . . . . . . . . . . . . . .
12.6 Desargues’ Theorem . . . . . . . . . . . . . . . . . . . . . . . . .
13 Symmedian . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
14 Homothety
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
14.1 Homothetic center of circles . . . . . . . . . . . . . . . . . . . . .
14.2 Composition of homotheties . . . . . . . . . . . . . . . . . . . . .
14.3 Useful Lemmas . . . . . . . . . . . . . . . . . . . . . . . . . . . .
15 Inversion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
16 Pole & Polar . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
17 Complete quadrilateral . . . . . . . . . . . . . . . . . . . . . . . . .
17.1 Cyclic Quadrilateral
. . . . . . . . . . . . . . . . . . . . . . . . . 102
18 Harmonic Ratio . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 106
18.1 Harmonic Pencil
. . . . . . . . . . . . . . . . . . . . . . . . . . . 109
18.2 Harmonic Quadrilateral
. . . . . . . . . . . . . . . . . . . . . . . 111
18.3 Useful Lemmas . . . . . . . . . . . . . . . . . . . . . . . . . . . . 114
19 Feuerbach’s Theorem . . . . . . . . . . . . . . . . . . . . . . . . . . 118
20 Apollonius’ Problem
. . . . . . . . . . . . . . . . . . . . . . . . . . 120
II
Mixed Problems
Bibliography . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 133
ii

### [Trang 9 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Introduction
This book is aimed at anyone who wishes to prepare for the geometry part of
the mathematics competitions and Olympiads around the world. No previous
knowledge of geometry is needed. Even though I am a fan of non-linear sto-
rytelling, this book progresses in a linear way, so everything that you need to
know at a certain point will have been already visited before. We will start our
journey with the most basic topics and gradually progress towards the more
advanced ones. The level ranges from junior competitions in your local area,
through senior national Olympiads around the world, to the most prestigious
International Mathematical Olympiad.
The word ”Beautiful” in the book’s title means that we will explore only
synthetic approaches and proofs, which I ﬁnd elegant and beautiful. We will
not see any analytic approaches, such as Cartesian or barycentric coordinates,
nor we will do complex number or trigonometry bashing.
Structure
This book is structured in two parts. The ﬁrst one provides an introduction
to concepts and theorems.
For the purpose of applying these concepts and
theorems to geometry problems, a number of useful properties and examples
with solutions are oﬀered. At the end of each chapter, a selection of unsolved
problems is provided as an exercise and a challenge for the reader to test their
skills in relation to the chapter topics. The second part contains mixed problems,
mostly from competitions and Olympiads from all around the world.
Acknowledgments
I would like to thank my primary school math teacher Ms. Vesna Todorovikj for
her dedication in training me and my friend Bojan Joveski for the national math
competitions. She introduced me to problem solving and thinking logically, in
general. I’ll never forget the handwritten collection of geometry problems that
she gave us, which made me start loving geometry.
I would also like to thank my high school math Olympiad mentor, Mr.
¨Ozg¨ur Kır¸cak.
He boosted my Olympiad spirit during the many Saturdays
in ”Olympiad Room” while eating burek, drinking tea and solving Olympiad
problems. Under his guidance, I started preparing geometry worksheets and
teaching the younger Olympiad students. Those worksheets are the foundation
of this book.
v

### [Trang 10 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Stefan Lozanovski
Finally, I would like to thank all of my students for working through the
geometry worksheets, shaping the Olympiad geometry curriculum together with
me and giving honest feedback about the lessons and about me as a teacher.
Their enthusiasm for geometry and thirst for more knowledge were a great
inspiration for me to write this book.
Support & Feedback
This book is part of my project for sharing knowledge with the whole world. If
you are satisﬁed with the book contents, please support the project by donating
at olympiadgeometry.com.
Tell me what you think about the book and help me make this Journey even
more beautiful. Write a general comment about the book, suggest a topic you’d
like to see covered in a future version or report a mistake at the same web site.
You can also follow us on Facebook (facebook.com/olympiadgeometry) for
the latest news and updates. Please leave you honest review there.
The Author
vi

### [Trang 11 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
A Beautiful Journey Through Olympiad Geometry
Notations
Since the math notations slightly diﬀer in various regions of the world, here is
a quick summary of the ones we are going to use throughout our journey.
Notation
Explanation
∠ABC
angle ABC; or measurement of said angle
AB
length of the line segment AB
−−→
AB
vector AB
˜
AB
arc AB
(ABCD)
circumcircle of the cyclic polygon ABCD
≡
coincide
Example: if A −B −C are collinear, then AB ≡AC.
∩
intersection
⊥
perpendicular
∥
parallel
P△ABC
area of the triangle ABC
PABCD
area of the polygon ABCD
d(P, AB)
distance from the point P to the line AB
∠(p, q)
angle between the lines p and q
α, β, γ, . . .
unless otherwise noted, the angles at the vertices A, B, C, . . . in a
polygon ABC . . . ; or measurements of said angles
a, b, c
unless otherwise noted, the sides opposite the vertices A, B, C in
a triangle ABC; or lengths of said sides
⇐⇒
if and only if (shortened iﬀ)
Example: p ⇐⇒q means ”if p then q AND if q then p”.
∴
therefore
∵
because
LHS \ RHS
The left-hand side \ the right-hand side of an equation
WLOG
Without loss of generality
■
Q.E.D. (initialism of the Latin phrase ”quod erat demonstran-
dum”, meaning ”which is what had to be proved”.)
vii

### [Trang 15 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Chapter 1
Congruence of Triangles
Two triangles △ABC and △A1B1C1 are said to be congruent when their cor-
responding sides and corresponding angles are equal.
Figure 1.1: Congruent triangles.
△ABC ∼= △A1B1C1 ⇐⇒a = a1, b = b1, c = c1, α = α1, β = β1, γ = γ1
However, in most of the problems, the equality of all these six pairs of elements
will not be given, so we will need to use some criteria for congruence. With
these criteria, we will prove the congruence of two triangles only by using the
equality of three pairs of corresponding elements.
Criterion SSS (side-side-side) If three pairs of corresponding sides are equal,
then the triangles are congruent.
Criterion SAS (side-angle-side) If two pairs of corresponding sides and the
angles between them are equal, then the triangles are congruent.
Criterion ASA (angle-side-angle) If two pairs of corresponding angles and
the sides formed by the common rays of these angles are equal, then the
triangles are congruent.
These criteria are part of our axioms, so we will not prove them. However, in
Figure 1.2, you can see that we can construct exactly one triangle given the
corresponding set of elements for each criteria. We can also see why there can
not exist an ASS congruence criterion.

### [Trang 17 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Chapter 2
Angles of a Transversal
When two lines p and q are intersected by a third line t, we get eight angles. The
line t is called a transversal. The pairs of angles, depending on their position
relative to the transversal and the two given lines are called:
corresponding angles if they lie on the same side of the transversal and one
of them is in the interior of the lines p and q, while the other one is in the
exterior (e.g. α1 and α2);
alternate angles if they lie on diﬀerent side of the transversal and both of
them are either in the interior or in the exterior of the lines p and q (e.g.
β1 and β2); or
opposite1angles if they lie on the same side of the transversal and both of
them are either in the interior or in the exterior of the lines p and q (e.g.
γ1 and γ2).
Figure 2.1: Angles of a transversal.
1In some resources, the interior opposite angles are called consecutive interior angles, but
there is no name for the exterior opposite angles, which have the same property. Since in
some languages these angles are called opposite, in this book we’ll call them that in English,
too, even though I haven’t seen this terminology used in other resources in English.

### [Trang 18 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Stefan Lozanovski
Property 2.1. If the lines p and q are parallel, then the corresponding angles
are equal, the alternate angles are equal and the opposite angles are supplemen-
tary. The converse is also true.
p ∥q ⇐⇒α1 = α2, β1 = β2, γ1 + γ2 = 180◦
Proof. Let the transversal t intersect p and q at A and B, respectively and let
O be the midpoint of the line segment AB, i.e. AO = BO. Let r be a line
through O that is perpendicular to p. Let r ∩p = C and r ∩q = D. Then
∠OCA = 90◦. Let’s prove one of the directions, i.e. let ∠OAC = ∠OBD. The
angles ∠AOC and ∠BOD are vertical angles and therefore equal. So, by the
criterion ASA, △AOC ∼= △BOD. Therefore, their corresponding elements are
equal, i.e. ∠ODB = ∠OCA = 90◦. So, r ⊥q. Therefore, p ∥q. □
Now, let’s prove the other direction. Let p ∥q. Let t be a transversal, such
that t ∩p = A and t ∩q = B. Let C ∈p and D ∈q, such that C and D are
on diﬀerent sides of t. We want to prove that ∠BAC = ∠ABD. Let D′ be a
point such that ∠BAC = ∠ABD′. By the direction we just proved, AC ∥BD′.
Since B lies on both BD and BD′ and BD′ ∥AC ∥BD, then BD ≡BD′ and
consequently, ∠ABD ≡∠ABD′. Therefore, ∠BAC = ∠ABD.
Remark. The other angles with vertices at A and B are either vertical to (and
therefore equal) or form a linear pair (and therefore supplementary) with the
angles ∠BAC and ∠ABD, so it is easy to prove the rest.
■

### [Trang 19 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
A Beautiful Journey Through Olympiad Geometry
Example 2.1 (Sum of angles in a triangle). Prove that the sum of the interior
angles in a triangle is 180 degrees.
Proof. Let ABC be a triangle. Let’s draw a line B1A1 which passes through C
and is parallel to AB. Then, by Property 2.1, we have:
∠B1CA = ∠CAB = α
(alternate interior angles; transversal AC)
∠A1CB = ∠CBA = β
(alternate interior angles; transversal BC)
∠ACB = γ
∴
∠B1CA + ∠A1CB + ∠ACB = α + β + γ
∠B1CA1 = α + β + γ
180◦= α + β + γ
■
Example 2.2. Prove that an exterior angle equals the sum of the two non-
adjacent interior angles.
Proof. Let ABC be a triangle and let A1 be a point on the extension of AB.
∠A1BC + ∠ABC = 180◦
(linear pair)
∠ABC + ∠BCA + ∠CAB = 180◦
(Sum of angles in a triangle)
∴
∠A1BC = 180◦−∠ABC = ∠BCA + ∠CAB
■
Example 2.3. Find the sum of the interior angles in an n-gon.
Proof. Let A1A2A3 . . . An be a polygon with n
sides. If we draw the diagonals from A1 to all
the other (n−3) vertices, we get (n−2) distinct
triangles. By Example 2.1, the sum of all the
interior angles in these triangles is (n−2)·180◦.
Note that these angles actually form all the in-
terior angles in the n-gon. So, the sum of the
interior angles in an n-gon is (n −2) · 180◦.
■

### [Trang 20 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Stefan Lozanovski
Example 2.4. Find the sum of the exterior angles in an n-gon.
Proof. Let A1A2A3 . . . An be a polygon with n sides. Let αi and ϕi (i = 1, 2, . . . , n)
be the interior and exterior angles in the polygon, respectively.
Since each exterior and its corresponding interior angle form a linear pair, we
have αi + βi = 180◦, i = 1, 2, . . . , n. If we sum these equations, we get
n
X
i=1
αi +
n
X
i=1
ϕi = n · 180◦.
From Example 2.3, we know that
n
X
i=1
αi = (n −2) · 180◦.
In order to ﬁnd the sum of the exterior angles, we need to subtract the two
previous equations.
n
X
i=1
ϕi =  n −(n −2) · 180◦= 2 · 180◦= 360◦.
So, the sum of the exterior angles in any polygon does not depend on the number
of sides n and is always 360◦.
■
Example 2.5 (Isosceles Triangle). In △ABC, two of the sides are equal, i.e.
CA = CB. Prove that ∠CAB = ∠CBA.
Proof. Let the angle bisector of ∠BCA intersect the side
AB at M.
Then, ∠ACM = ∠BCM.
Combining with
CA = CB and CM-common side, by SAS, we get that
△ACM ∼= △BCM. Therefore, their corresponding angles
are equal, i.e.
∠CAB ≡∠CAM = ∠CBM ≡∠CBA.
Additionally, as a consequence of the congruence, we can
also get two other things:
AM = MB and ∠AMC =
∠BMC, which means that CM ⊥AB.
Therefore, as a
conclusion, the angle bisector, the median and the altitude
from the vertex C in an isosceles triangle coincide with the
side bisector of AB.
■
Remark. The converse is also true (if ∠CAB = ∠CBA, then CA = CB). Can
you prove it by yourself?

### [Trang 21 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
A Beautiful Journey Through Olympiad Geometry
Example 2.6 (Equilateral triangle). In △ABC, all three sides are equal. Prove
that all the angles are equal to 60◦.
Proof. Combining Example 2.1 and Example 2.5, we directly get the desired
result.
■
Example 2.7. In any triangle, a greater side subtends a greater angle.
Proof. In △ABC, let AC > AB. Then we can choose a point D on the side
AC, such that AD = AB. Since △ABD is isosceles, we have ∠ABD = ∠ADB.
∠ABC > ∠ABD = ∠ADB
2.2
= ∠DBC + ∠DCB > ∠DCB ≡∠ACB
■
Example 2.8. In any triangle, a greater angle is subtended by a greater side.
Proof. In △ABC, let ∠ABC > ∠ACB. We want to prove that AC > AB.
Let’s assume the opposite, i.e. AC ≤AB.
i) If AC = AB, then by Example 2.5, ∠ABC = ∠ACB, which is not true.
ii) If AC < AB, then by Example 2.7, ∠ABC < ∠ACB, which is not true.
Therefore, our assumption is wrong, so AC > AB.
■
Example 2.9 (Triangle Inequality). In any triangle, the sum of the lengths of
any two sides is greater than the length of the third side.
Proof. In △ABC, let D be a point on the extension of the side BC beyond C,
such that CD = CA. Then, △CAD is isosceles, so ∠CAD = ∠CDA. Now, in
△BAD we have
∠BAD = ∠BAC + ∠CAD > ∠CAD = ∠CDA ≡∠BDA,
which by Example 2.8 means that BD > AB. Therefore,
BC + CA = BC + CD = BD > AB
■

### [Trang 22 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Stefan Lozanovski
Example 2.10. Let ABCD be a parallelogram. Prove that its opposite sides
are equal.
Proof. Let’s draw the diagonal AC. Since AB ∥CD, by Property 2.1, ∠CAB =
∠ACD. Similarly, since BC ∥AD, ∠ACB = ∠CAD. Therefore, since AC is
a common side for the triangles △ABC and △CDA, by the ASA criterion,
△ABC ∼= △CDA.
Therefore, their corresponding elements, are equal, i.e.
AB = CD and BC = DA.
■
Example 2.11. In the quadrilateral ABCD, the intersection point of the di-
agonals bisects them. Prove that ABCD is a parallelogram.
Proof. Let the intersection of the diagonals AC and BD be S.
Then, from
the condition, we have that AS = SC and BS = SD. Let’s take a look at
△ABS and △CDS. We have AS = CS, ∠ASB = ∠CSD as vertical angles
and BS = DS. So, by the SAS criterion, △ABS ∼= △CDS. Therefore, the
corresponding elements are equal, i.e. ∠ABS = ∠CDS. Since these angles
are alternate angles of the transversal BD and the lines AB and CD, we have
that AB ∥CD. Similarly, △BCS ∼= △DAS and ∠BCS = ∠DAS. Therefore,
BC ∥DA.
■
Example 2.12. In the quadrilateral ABCD, AB = CD and AB ∥CD. Prove
that ABCD is a parallelogram.
Proof. Let the intersection of the diagonals AC and BD be S. Since AB ∥CD,
the alternate angles of the transversal BD are equal, i.e. ∠ABS = ∠CDS.
Similarly, ∠BAS = ∠DCS. Combining with the fact that AB = CD, by the
ASA criterion, we get that △ABS ∼= △CDS. Therefore, as the corresponding
elements are equal, AS = CS and BS = DS. Combining with the fact that
∠ASD = ∠CSB as vertical angles, by the SAS criterion we get that △ASD ∼=
△CSB. Therefore, ∠DAS = ∠BCS, so DA ∥BC.
■

### [Trang 23 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
A Beautiful Journey Through Olympiad Geometry
Example 2.13 (Midsegment Theorem). In a triangle, the segment joining the
midpoints of any two sides is parallel to the third side and half its length.
Proof. In △ABC, let M and N be the midpoints of the sides AB and AC,
respectively. Let P be a point on the ray MN beyond N, such that MN = NP.
Since ∠MNA = ∠PNC as vertical angles, by SAS we have that △AMN ∼=
△CPN.
Therefore, AM = CP and ∠MAN = ∠PCN which means that
AM ∥CP. Now, we have BM = AM = CP and BM ≡AM ∥CP. By
Example 2.12, since the opposite sides in the quadrilateral MBCP are of equal
length and parallel, it must be a parallelogram. Therefore,
MN ≡MP ∥BC
and because of Example 2.10,
MN = 1
2MP = 1
2BC.
■
Related problems: 1, 2 and 6.

### [Trang 24 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Chapter 3
Area of Plane Figures
Rectangle
The area of a rectangle ABCD is deﬁned as the product of the length a =
AB = CD and the width b = BC = AD of the rectangle.
PABCD = a · b
Using this fact, we will derive the formulae for the area of other plane ﬁgures.
Parallelogram
Let ABCD be a parallelogram. WLOG, let ∠ABC > 90◦. Let C1 and D1
be the feet of the perpendiculars from C and D, respectively, to the line AB.
Since AD ∥BC, by Property 2.1, γ = 180◦−δ.
∠BCC1 = 90◦−γ = δ −90◦= ∠ADD1
Additionally, CC1 = d(AB, CD) = DD1 and ∠CC1B = 90◦= ∠DD1A.
Therefore, by the ASA criterion, △BCC1 ∼= △ADD1. So P△BCC1 = P△ADD1.
PABCD = P△ADD1 + PDD1BC = P△BCC1 + PDD1BC = PDD1C1C
Since DD1C1C is a rectangle with length CD = AB = a and width CC1 = ha,
we get
PABCD = a · ha


------------------------------------------------------------

## NGUỒN: IMO SHORTLIST 1959-2016 EN AOPS
- **Phân hệ:** [HÌNH HỌC PHẲNG OLYMPIC 2D]
- **Tên file:** `IMO Shortlist 1959-2016 EN aops.pdf` (274 trang)

### [Trang 1 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
IN THE NAME OF 
ALLAH 

IMO ShortList Problems 
1959 – 2009 

Collected by: Amir Hossein Parvardi (amparvardi) 

Problems from: 
http://www.artofproblemsolving.com/Forum/resources.php 

Published: 2010-10 

Email: amir_ahp_2009@yahoo.com

### [Trang 2 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Contents 

Year 
Page 
Number of Problems 
5 
6 ∗  
7 
1961 
6 
11 
1963 
6 
15 
1965 
6 
19 
1967 
59 
38 
1969 
71 
48 
1971 
17 
53 
1973 
17 
58 
1975 
15 
62 
1977 
16 
67 
1979 
26

### [Trang 3 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Year 
Page 
Number of Problems 
72 
1981 
19 
78 
1983 
25 
84 
1985 
22 
90 
1987 
23 
97 
1989 
32 
104 
1991 
30 
117 
1993 
26 
128 
1995 
28 
139 
1997 
26 
150 
1999 
27 
163 
2001 
28 
175 
2003 
27

### [Trang 4 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Year 
Page 
Number of Problems 
188 
2005 
27 
201 
2007 
30 
214 
2009 
30 

 ∗ ShortListed Problems of the years 1959 to 1966 were the same, so I just added those 
problems to the year 1966 and used IMO problems for the years 1959 – 1965. Thanks 
Orlando (orl) for this suggestion.

### [Trang 5 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
IMO 1959
Brasov and Bucharest, Romania
Day 1
Prove that the fraction 21n + 4
14n + 3 is irreducible for every natural number n.
For what real values of x is
q
x +
√
2x −1 +
q
x −
√
2x −1 = A
given
a) A =
√
2;
b) A = 1;
c) A = 2,
where only non-negative real numbers are admitted for square roots?
Let a, b, c be real numbers. Consider the quadratic equation in cos x
a cos x2 + b cos x + c = 0.
Using the numbers a, b, c form a quadratic equation in cos 2x whose roots are the same as
those of the original equation. Compare the equation in cos x and cos 2x for a = 4, b = 2,
c = −1.
http://www.artofproblemsolving.com/
This ﬁle was downloaded from the AoPS Math Olympiad Resources Page
Page 1

### [Trang 6 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
IMO 1959
Brasov and Bucharest, Romania
Day 2
Construct a right triangle with given hypotenuse c such that the median drawn to the hy-
potenuse is the geometric mean of the two legs of the triangle.
An arbitrary point M is selected in the interior of the segment AB. The square AMCD
and MBEF are constructed on the same side of AB, with segments AM and MB as their
respective bases.
The circles circumscribed about these squares, with centers P and Q,
intersect at M and also at another point N. Let N′ denote the point of intersection of the
straight lines AF and BC.
a) Prove that N and N′ coincide;
b) Prove that the straight lines MN pass through a ﬁxed point S independent of the choice
of M;
c) Find the locus of the midpoints of the segments PQ as M varies between A and B.
Two planes, P and Q, intersect along the line p. The point A is given in the plane P, and
the point C in the plane Q; neither of these points lies on the straight line p. Construct
an isosceles trapezoid ABCD (with AB ∥CD) in which a circle can be inscribed, and with
vertices B and D lying in planes P and Q respectively.
http://www.artofproblemsolving.com/
This ﬁle was downloaded from the AoPS Math Olympiad Resources Page
Page 2

### [Trang 7 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
IMO 1960
Sinaia, Romania
Day 1
Determine all three-digit numbers N having the property that N is divisible by 11, and N
is equal to the sum of the squares of the digits of N.
For what values of the variable x does the following inequality hold:
4x2
(1 −√2x + 1)2 < 2x + 9 ?
In a given right triangle ABC, the hypotenuse BC, of length a, is divided into n equal parts (n
and odd integer). Let α be the acute angel subtending, from A, that segment which contains
the mdipoint of the hypotenuse. Let h be the length of the altitude to the hypotenuse fo the
triangle. Prove that:
tan α =
4nh
(n2 −1)a.
http://www.artofproblemsolving.com/
This ﬁle was downloaded from the AoPS Math Olympiad Resources Page
Page 1

### [Trang 8 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
IMO 1960
Sinaia, Romania
Day 2
Construct triangle ABC, given ha, hb (the altitudes from A and B), and ma, the median
from vertex A.
Consider the cube ABCDA′B′C′D′ (with face ABCD directly above face A′B′C′D′).
a) Find the locus of the midpoints of the segments XY , where X is any point of AC and Y
is any piont of B′D′;
b) Find the locus of points Z which lie on the segment XY of part a) with ZY = 2XZ.
Consider a cone of revolution with an inscribed sphere tangent to the base of the cone. A
cylinder is circumscribed about this sphere so that one of its bases lies in the base of the cone.
let V1 be the volume of the cone and V2 be the volume of the cylinder.
a) Prove that V1̸ = V2;
b) Find the smallest number k for which V1 = kV2; for this case, construct the angle subtended
by a diamter of the base of the cone at the vertex of the cone.
An isosceles trapezoid with bases a and c and altitude h is given.
a) On the axis of symmetry of this trapezoid, ﬁnd all points P such that both legs of the
trapezoid subtend right angles at P;
b) Calculate the distance of p from either base;
c) Determine under what conditions such points P actually exist. Discuss various cases that
might arise.
http://www.artofproblemsolving.com/
This ﬁle was downloaded from the AoPS Math Olympiad Resources Page
Page 2

### [Trang 9 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
IMO 1961
Veszprem, Hungary
Day 1
Solve the system of equations:
x + y + z = a
x2 + y2 + z2 = b2
xy = z2
where a and b are constants. Give the conditions that a and b must satisfy so that x, y, z are
distinct positive numbers.
Let a, b, c be the sides of a triangle, and S its area. Prove:
a2 + b2 + c2 ≥4S
√
In what case does equality hold?
Solve the equation cosn x −sinn x = 1 where n is a natural number.
http://www.artofproblemsolving.com/
This ﬁle was downloaded from the AoPS Math Olympiad Resources Page
Page 1

### [Trang 10 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
IMO 1961
Veszprem, Hungary
Day 2
Consider triangle P1P2P3 and a point p within the triangle. Lines P1P, P2P, P3P intersect
the opposite sides in points Q1, Q2, Q3 respectively. Prove that, of the numbers
P1P
PQ1
, P2P
PQ2
, P3P
PQ3
at least one is ≤2 and at least one is ≥2
Construct a triangle ABC if AC = b, AB = c and ∠AMB = w, where M is the midpoint of
the segment BC and w < 90. Prove that a solution exists if and only if
b tan w
2 ≤c < b
In what case does the equality hold?
Consider a plane ϵ and three non-collinear points A, B, C on the same side of ϵ; suppose the
plane determined by these three points is not parallel to ϵ. In plane ϵ take three arbitrary
points A′, B′, C′. Let L, M, N be the midpoints of segments AA′, BB′, CC′; Let G be the
centroid of the triangle LMN. (We will not consider positions of the points A′, B′, C′ such
that the points L, M, N do not form a triangle.) What is the locus of point G as A′, B′, C′
range independently over the plane ϵ?
http://www.artofproblemsolving.com/
This ﬁle was downloaded from the AoPS Math Olympiad Resources Page
Page 2

### [Trang 11 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
IMO 1962
Ceske Budejovice, Czechoslovakia
Day 1
Find the smallest natural number n which has the following properties:
a) Its decimal representation has a 6 as the last digit.
b) If the last digit 6 is erased and placed in front of the remaining digits, the resulting number
is four times as large as the original number n.
Determine all real numbers x which satisfy the inequality:
√
3 −x −
√
x + 1 > 1
3
Consider the cube ABCDA′B′C′D′ (ABCD and A′B′C′D′ are the upper and lower bases,
repsectively, and edges AA′, BB′, CC′, DD′ are parallel). The point X moves at a constant
speed along the perimeter of the square ABCD in the direction ABCDA, and the point Y
moves at the same rate along the perimiter of the square B′C′CB in the direction B′C′CBB′.
Points X and Y begin their motion at the same instant from the starting positions A and B′,
respectively. Determine and draw the locus of the midpionts of the segments XY .
http://www.artofproblemsolving.com/
This ﬁle was downloaded from the AoPS Math Olympiad Resources Page
Page 1

### [Trang 12 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
IMO 1962
Ceske Budejovice, Czechoslovakia
Day 2
Solve the equation cos2 x + cos2 2x + cos2 3x = 1
On the circle K there are given three distinct points A, B, C. Construct (using only a straight-
edge and a compass) a fourth point D on K such that a circle can be inscribed in the quadri-
lateral thus obtained.
Consider an isosceles triangle. let R be the radius of its circumscribed circle and r be the
radius of its inscribed circle. Prove that the distance d between the centers of these two circle
is
d =
p
R(R −2r)
The tetrahedron SABC has the following property: there exist ﬁve spheres, each tangent to
the edges SA, SB, SC, BC, CA, AB, or to their extensions.
a) Prove that the tetrahedron SABC is regular.
b) Prove conversely that for every regular tetrahedron ﬁve such spheres exist.
http://www.artofproblemsolving.com/
This ﬁle was downloaded from the AoPS Math Olympiad Resources Page
Page 2

### [Trang 13 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
IMO 1963
Warsaw, Poland
Day 1
Find all real roots of the equation
p
x2 −p + 2
p
x2 −1 = x
where p is a real parameter.
Point A and segment BC are given. Determine the locus of points in space which are vertices
of right angles with one side passing through A, and the other side intersecting segment BC.
In an n-gon A1A2 . . . An, all of whose interior angles are equal, the lengths of consecutive
sides satisfy the relation
a1 ≥a2 ≥· · · ≥an.
Prove that a1 = a2 = . . . = an.
http://www.artofproblemsolving.com/
This ﬁle was downloaded from the AoPS Math Olympiad Resources Page
Page 1

### [Trang 14 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
IMO 1963
Warsaw, Poland
Day 2
Find all solutions x1, x2, x3, x4, x5 of the system
x5 + x2 = yx1
x1 + x3 = yx2
x2 + x4 = yx3
x3 + x5 = yx4
x4 + x1 = yx5
where y is a parameter.
Prove that cos π
7 −cos 2π
7 + cos 3π
7 = 1
6
Five students A, B, C, D, E took part in a contest. One prediction was that the contestants
would ﬁnish in the order ABCDE. This prediction was very poor. In fact, no contestant
ﬁnished in the position predicted, and no two contestants predicted to ﬁnish consecutively
actually did so. A second prediction had the contestants ﬁnishing in the order DAECB. This
prediction was better. Exactly two of the contestants ﬁnished in the places predicted, and
two disjoint pairs of students predicted to ﬁnish consecutively actually did so. Determine the
order in which the contestants ﬁnished.
http://www.artofproblemsolving.com/
This ﬁle was downloaded from the AoPS Math Olympiad Resources Page
Page 2

### [Trang 15 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
IMO 1964
Moscow, USSR
Day 1
Suppose a, b, c are the sides of a triangle. Prove that
a2(b + c −a) + b2(a + c −b) + c2(a + b −c) ≤3abc
A circle is inscribed in a triangle ABC with sides a, b, c. Tangents to the circle parallel to the
sides of the triangle are contructe. Each of these tangents cuts oﬀa triagnle from △ABC.
In each of these triangles, a circle is inscribed. Find the sum of the areas of all four inscribed
circles (in terms of a, b, c).
http://www.artofproblemsolving.com/
This ﬁle was downloaded from the AoPS Math Olympiad Resources Page
Page 1


------------------------------------------------------------

## NGUỒN: IMO SHORTLIST OFFICIAL 1992-00 EN WITH SOLUTIONS, SCANNED
- **Phân hệ:** [HÌNH HỌC PHẲNG OLYMPIC 2D]
- **Tên file:** `IMO Shortlist Official 1992-00 EN with solutions, scanned.pdf` (444 trang)


------------------------------------------------------------

## NGUỒN: IMO SHORTLIST OFFICIAL 2001-10 EN WITH SOLUTIONS
- **Phân hệ:** [HÌNH HỌC PHẲNG OLYMPIC 2D]
- **Tên file:** `IMO Shortlist Official 2001-10 EN with solutions.pdf` (618 trang)

### [Trang 1 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Contents
Problems
1.1
Algebra
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
1.2
Combinatorics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
1.3
Geometry . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
1.4
Number Theory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
2
Algebra
A1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
A2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
A3 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
A4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
A5 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
A6 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
3
Combinatorics
C1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C3 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C5 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C6 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
C7 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
i

### [Trang 2 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
ii
CONTENTS
C8 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
4
Geometry
G1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
G2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
G3 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
G4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
G5 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
G6 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
G7 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
G8 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
5
Number Theory
N1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
N2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
N3 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
N4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
N5 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
N6 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

### [Trang 3 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Chapter 1
Problems
1.1
Algebra
A1. Let T denote the set of all ordered triples (p, q, r) of nonnegative integers. Find
all functions f : T →R such that
f(p, q, r) =











if pqr = 0,
1 + 1
6{f(p + 1, q −1, r) + f(p −1, q + 1, r)
+f(p −1, q, r + 1) + f(p + 1, q, r −1)
+f(p, q + 1, r −1) + f(p, q −1, r + 1)}
otherwise.
A2. Let a0, a1, a2, . . . be an arbitrary inﬁnite sequence of positive numbers. Show
that the inequality 1 + an > an−1
n√
2 holds for inﬁnitely many positive integers n.
A3. Let x1, x2, . . . , xn be arbitrary real numbers. Prove the inequality
x1
1 + x2
+
x2
1 + x2
1 + x2
+ · · · +
xn
1 + x2
1 + · · · + x2
n
< √n.

### [Trang 4 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
2
CHAPTER 1. PROBLEMS
A4. Find all functions f : R →R, satisfying
f(xy)(f(x) −f(y)) = (x −y)f(x)f(y)
for all x, y.
A5. Find all positive integers a1, a2, . . . , an such that
100 = a0
a1
+ a1
a2
+ · · · + an−1
an
,
where a0 = 1 and (ak+1 −1)ak−1 ≥a2
k(ak −1) for k = 1, 2, . . . , n −1.
A6. Prove that for all positive real numbers a, b, c,
a
√
a2 + 8bc +
b
√
b2 + 8ca +
c
√
c2 + 8ab ≥1.

### [Trang 5 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
1.2. COMBINATORICS
1.2
Combinatorics
C1. Let A = (a1, a2, . . . , a2001) be a sequence of positive integers. Let m be the
number of 3-element subsequences (ai, aj, ak) with 1 ≤i < j < k ≤2001, such that
aj = ai + 1 and ak = aj + 1. Considering all such sequences A, ﬁnd the greatest value
of m.
C2. Let n be an odd integer greater than 1 and let c1, c2, . . . , cn be integers. For each
permutation a = (a1, a2, . . . , an) of {1, 2, . . . , n}, deﬁne S(a) = Pn
i=1 ciai. Prove that
there exist permutations a̸ = b of {1, 2, . . . , n} such that n! is a divisor of S(a)−S(b).
C3.
Deﬁne a k-clique to be a set of k people such that every pair of them are
acquainted with each other. At a certain party, every pair of 3-cliques has at least
one person in common, and there are no 5-cliques. Prove that there are two or fewer
people at the party whose departure leaves no 3-clique remaining.
C4. A set of three nonnegative integers {x, y, z} with x < y < z is called historic if
{z −y, y −x} = {1776, 2001}. Show that the set of all nonnegative integers can be
written as the union of pairwise disjoint historic sets.
C5. Find all ﬁnite sequences (x0, x1, . . . , xn) such that for every j, 0 ≤j ≤n, xj
equals the number of times j appears in the sequence.

### [Trang 6 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
4
CHAPTER 1. PROBLEMS
C6. For a positive integer n deﬁne a sequence of zeros and ones to be balanced if it
contains n zeros and n ones. Two balanced sequences a and b are neighbors if you
can move one of the 2n symbols of a to another position to form b. For instance,
when n = 4, the balanced sequences 01101001 and 00110101 are neighbors because
the third (or fourth) zero in the ﬁrst sequence can be moved to the ﬁrst or second
position to form the second sequence. Prove that there is a set S of at most
n+1
¡2n
n
¢
balanced sequences such that every balanced sequence is equal to or is a neighbor of
at least one sequence in S.
C7. A pile of n pebbles is placed in a vertical column. This conﬁguration is modiﬁed
according to the following rules. A pebble can be moved if it is at the top of a column
which contains at least two more pebbles than the column immediately to its right.
(If there are no pebbles to the right, think of this as a column with 0 pebbles.) At
each stage, choose a pebble from among those that can be moved (if there are any)
and place it at the top of the column to its right. If no pebbles can be moved, the
conﬁguration is called a ﬁnal conﬁguration. For each n, show that, no matter what
choices are made at each stage, the ﬁnal conﬁguration obtained is unique. Describe
that conﬁguration in terms of n.
Alternative Version.
A pile of 2001 pebbles is placed in a vertical column.
This
conﬁguration is modiﬁed according to the following rules. A pebble can be moved if
it is at the top of a column which contains at least two more pebbles than the column
immediately to its right. (If there are no pebbles to the right, think of this as a column
with 0 pebbles.) At each stage, choose a pebble from among those that can be moved
(if there are any) and place it at the top of the column to its right. If no pebbles can
be moved, the conﬁguration is called a ﬁnal conﬁguration. Show that, no matter what
choices are made at each stage, the ﬁnal conﬁguration obtained is unique. Describe
that conﬁguration as follows: Determine the number, c, of nonempty columns, and for
each i = 1, 2, . . . , c, determine the number of pebbles pi in column i, where column 1

### [Trang 7 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
1.2. COMBINATORICS
is the leftmost column, column 2 the next to the right, and so on.
C8. Twenty-one girls and twenty-one boys took part in a mathematical competition.
It turned out that
(a) each contestant solved at most six problems, and
(b) for each pair of a girl and a boy, there was at least one problem that was solved
by both the girl and the boy.
Show that there is a problem that was solved by at least three girls and at least three
boys.

### [Trang 8 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
6
CHAPTER 1. PROBLEMS
1.3
Geometry
G1. Let A1 be the center of the square inscribed in acute triangle ABC with two
vertices of the square on side BC. Thus one of the two remaining vertices of the
square is on side AB and the other is on AC. Points B1, C1 are deﬁned in a similar
way for inscribed squares with two vertices on sides AC and AB, respectively. Prove
that lines AA1, BB1, CC1 are concurrent.
G2. In acute triangle ABC with circumcenter O and altitude AP, ∠C ≥∠B + 30◦.
Prove that ∠A + ∠COP < 90◦.
G3. Let ABC be a triangle with centroid G. Determine, with proof, the position of
the point P in the plane of ABC such that AP·AG+BP·BG+CP·CG is a minimum,
and express this minimum value in terms of the side lengths of ABC.
G4. Let M be a point in the interior of triangle ABC. Let A′ lie on BC with MA′
perpendicular to BC. Deﬁne B′ on CA and C′ on AB similarly. Deﬁne
p(M) = MA′ · MB′ · MC′
MA · MB · MC .
Determine, with proof, the location of M such that p(M) is maximal. Let µ(ABC)
denote this maximum value. For which triangles ABC is the value of µ(ABC) max-
imal?

### [Trang 9 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
1.3. GEOMETRY
G5. Let ABC be an acute triangle. Let DAC, EAB, and FBC be isosceles triangles
exterior to ABC, with DA = DC, EA = EB, and FB = FC, such that
∠ADC = 2∠BAC,
∠BEA = 2∠ABC,
∠CFB = 2∠ACB.
Let D′ be the intersection of lines DB and EF, let E′ be the intersection of EC and
DF, and let F ′ be the intersection of FA and DE. Find, with proof, the value of the
sum
DB
DD′ + EC
EE′ + FA
FF ′.
G6. Let ABC be a triangle and P an exterior point in the plane of the triangle.
Suppose AP, BP, CP meet the sides BC, CA, AB (or extensions thereof) in D, E, F,
respectively. Suppose further that the areas of triangles PBD, PCE, PAF are all
equal. Prove that each of these areas is equal to the area of triangle ABC itself.
G7. Let O be an interior point of acute triangle ABC. Let A1 lie on BC with OA1
perpendicular to BC. Deﬁne B1 on CA and C1 on AB similarly. Prove that O is the
circumcenter of ABC if and only if the perimeter of A1B1C1 is not less than any one
of the perimeters of AB1C1, BC1A1, and CA1B1.
G8. Let ABC be a triangle with ∠BAC = 60◦. Let AP bisect ∠BAC and let BQ
bisect ∠ABC, with P on BC and Q on AC. If AB + BP = AQ + QB, what are the
angles of the triangle?

### [Trang 10 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
8
CHAPTER 1. PROBLEMS
1.4
Number Theory
N1.
Prove that there is no positive integer n such that, for k = 1, 2, . . . , 9, the
leftmost digit (in decimal notation) of (n + k)! equals k.
N2. Consider the system
x + y = z + u
2xy = zu.
Find the greatest value of the real constant m such that m ≤x/y for any positive
integer solution (x, y, z, u) of the system, with x ≥y.
N3. Let a1 = 1111, a2 = 1212, a3 = 1313, and
an = |an−1 −an−2| + |an−2 −an−3|,
n ≥4.
Determine a1414.
N4.
Let p ≥5 be a prime number.
Prove that there exists an integer a with
1 ≤a ≤p −2 such that neither ap−1 −1 nor (a + 1)p−1 −1 is divisible by p2.
N5. Let a > b > c > d be positive integers and suppose
ac + bd = (b + d + a −c)(b + d −a + c).
Prove that ab + cd is not prime.
N6. Is it possible to ﬁnd 100 positive integers not exceeding 25,000, such that all
pairwise sums of them are diﬀerent?

### [Trang 11 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Chapter 2
Algebra
Problem A1. Let T denote the set of all ordered triples (p, q, r) of nonnegative
integers. Find all functions f : T →R such that
f(p, q, r) =











if pqr = 0,
1 + 1
6{f(p + 1, q −1, r) + f(p −1, q + 1, r)
+f(p −1, q, r + 1) + f(p + 1, q, r −1)
+f(p, q + 1, r −1) + f(p, q −1, r + 1)}
otherwise.
Solution. First, we will show that there is at most one function which satisﬁes the
given conditions. Suppose that f1 and f2 are two such functions. Deﬁne h = f1 −f2.
Then h : T →R satisﬁes
h(p, q, r) =











if pqr = 0,
6{h(p + 1, q −1, r) + h(p −1, q + 1, r)
+h(p −1, q, r + 1) + h(p + 1, q, r −1)
+h(p, q + 1, r −1) + h(p, q −1, r + 1)}
otherwise.
Observe that the second condition states that h(p, q, r) is equal to the average of the
values of h at the six points (p + 1, q −1, r), etc., which are the vertices of a regular
hexagon with center at (p, q, r) lying in the plane x + y + z = p + q + r. It suﬃces to
show that h = 0 for all points in T. Let n be a positive integer. Consider the subset H

### [Trang 12 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
10
CHAPTER 2. ALGEBRA
of the plane x+y+z = n that lies in the “nonnegative” octant {(x, y, z) : x, y, z ≥0}.
Suppose h attains its maximum on H ∩T at (p, q, r). If pqr = 0 then the maximum
value for h on H ∩T is 0. If pqr̸ = 0, the averaging property of h implies that the
values of h on the six points (p + 1, q −1, r), etc. are all equal to h(p, q, r). (The six
points are all in H). In particular, h also attains its maximum at (p + 1, q −1, r).
Repeating the argument (if necessary) using (p + 1, q −1, r) as the center point,we
see that
h(p, q, r) = h(p + 1, q −1, r) = h(p + 2, q −2, r).
Continuing this process, we conclude that h(p, q, r) = h(p + q, 0, r) = 0. Thus the
maximum value of h on H ∩T is 0. By applying the same argument to the function
−h = f2 −f1, we see that the minimum value attained by h on H ∩T is also 0. Thus
h = 0 for all points in H ∩T. Varying n, we conclude that h = 0 on all points in T.
We will complete the solution by noting that f : T →R deﬁned by
f(p, q, r) =





if pqr = 0,
3pqr
p + q + r
otherwise
satisﬁes both conditions of the problem, and is the unique solution.
Remark 1. One can guess the solution function in the following way: For any function
f deﬁned on T, deﬁne the function A[f] by
A[f](p, q, r) = 1
6 (f(p + 1, q −1, r) + · · · ) .
It is easy to check that if c is a constant, then
A[cf] = cA[f]
and
A[c + f] = c + A[f].
Also note that if h is deﬁned by h(p, q, r) = f(p, q, r)/(p + q + r), then
A[h](p, q, r) = A[f](p, q, r)
p + q + r .

### [Trang 13 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
11
We need to ﬁnd a function f that satisﬁes the boundary conditions, as well as the
second condition
f = A[f] + 1.
It is natural to start by considering g(p, q, r) = pqr, which satisﬁes the boundary
conditions. We shall suitably modify this so that the second condition is also satisﬁed.
Observe that
A[g](p, q, r) = 1
6 (6pqr −2(p + q + r)) = g(p, q, r) −p + q + r
.
Thus there is an extra term involving p + q + r. To take care of this, we divide pqr
by p + q + r and consider the function u(p, q, r) = pqr/(p + q + r). We have
A[u](p, q, r) = A[g](p, q, r)
p + q + r
= u(p, q, r) −1
3.
Thus
A[3u] = 3u −1,
and hence 3pqr/(p + q + r) satisﬁes the second condition.
Remark 2.
One can consider the two-dimensional version of this problem, where
f(p, q) = 0 if pq = 0 and f(p, q) = 1 + [f(p + 1, q −1) + f(p −1, q + 1)]/2 otherwise.
The unique solution is f(p, q) = pq.

### [Trang 14 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
12
CHAPTER 2. ALGEBRA
Problem A2. Let a0, a1, a2, . . . be an arbitrary inﬁnite sequence of positive numbers.
Show that the inequality 1 + an > an−1
n√
2 holds for inﬁnitely many positive integers
n.
Solution 1. Let c0, c1, c2, c3, . . . be the sequence deﬁned by c0 = 1 and
cn =
µ an−1
1 + an
¶
cn−1,
n ≥1.
Rewriting this as cn = an−1cn−1 −ancn, we obtain the telescoping sum
c1 + c2 + · · · + cn = a0 −ancn.
(∗)
The assertion of the problem is equivalent to: cn/cn−1 < 2−1/n for inﬁnitely many n.
Assume to the contrary that there exists N such that the opposite inequality holds
for all n ≥N. Then for n > N,
cn ≥cN·2−(
N+1+
N+2+···+ 1
n) = C·2−(1+ 1
2 +···+ 1
n),
where C = cN·21+ 1
2+···+ 1
N is a positive constant. If 2k−1 ≤n < 2k, then
1 + 1
2 + · · · + 1
n ≤1 +
µ1
2 + 1
¶
+
µ1
4 + · · · + 1
¶
+ · · · +
µ 1
2k−1 + · · · +
2k −1
¶
≤1 + 1 + 1 + · · · + 1
= k,
so that
cn ≥C · 2−k
for
2k−1 ≤n < 2k.
Let r be such that 2r−1 ≤N < 2r, and let m > r. Then
c2r + c2r+1 + · · · + c2m−1 = (c2r + · · · + c2r+1−1) + (c2r+1 + · · · + c2r+2−1)
+ · · · + (c2m−1 + · · · + c2m−1)
≥C · (2r · 2−r−1 + 2r+1 · 2−r−2 + · · · + 2m−1 · 2−m)
= C · (m −r)
,

### [Trang 15 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
13
showing that the sum of the cn can be made arbitrarily large. However, by (∗), this
sum can never exceed a0. This contradiction shows that cn/cn−1 < 2−1/n for inﬁnitely
many n, as desired.
Solution 2. Arguing by contradiction, suppose there is N such that 1+an ≤an−121/n
for n ≥N. Multiply both sides by
bn = 2−(1+ 1
2 +···+ 1
n)
to get
bn + An ≤An−1,
where An = bnan.
Thus we have
bN ≤AN−1 −AN
bN+1 ≤AN −AN+1
...
...
...
bn ≤An−1 −An,
and thus
n
X
j=N
bj ≤AN−1 −An ≤AN−1,
since the aj are positive.
We shall show, however, that
X
n≥N
bn
diverges. To see this, note that because 1/x is monotone decreasing, a simple com-
parison of areas yields
2 + 1
3 + · · · + 1
n <
Z n
dx
x = log n,


------------------------------------------------------------

## NGUỒN: IMO SHORTLIST OFFICIAL 2011-20 EN WITH SOLUTIONS
- **Phân hệ:** [HÌNH HỌC PHẲNG OLYMPIC 2D]
- **Tên file:** `IMO Shortlist Official 2011-20 EN with solutions.pdf` (822 trang)

### [Trang 1 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
52
nd International 
Mathematical Olympiad
12 – 24 July 2011
         Amsterdam
The Netherlands
International
Mathematical
Olympiad Am
sterdam 2011 
IMO2011
Amsterdam
Problem Shortlist
with Solutions

### [Trang 2 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
52nd International
Mathematical Olympiad
12-24 July 2011
Amsterdam
The Netherlands
Problem shortlist
with solutions

### [Trang 4 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
IMPORTANT
IMO regulation:
these shortlist problems have to
be kept strictly conﬁdential
until IMO 2012.
The problem selection committee
Bart de Smit (chairman), Ilya Bogdanov, Johan Bosman,
Andries Brouwer, Gabriele Dalla Torre, G´eza K´os,
Hendrik Lenstra, Charles Leytem, Ronald van Luijk,
Christian Reiher, Eckard Specht, Hans Sterk, Lenny Taelman
The committee gratefully acknowledges the receipt of 142 problem proposals
by the following 46 countries:
Armenia, Australia, Austria, Belarus, Belgium,
Bosnia and Herzegovina, Brazil, Bulgaria, Canada, Colombia,
Cyprus, Denmark, Estonia, Finland, France, Germany, Greece,
Hong Kong, Hungary, India, Islamic Republic of Iran, Ireland, Israel,
Japan, Kazakhstan, Republic of Korea, Luxembourg, Malaysia,
Mexico, Mongolia, Montenegro, Pakistan, Poland, Romania,
Russian Federation, Saudi Arabia, Serbia, Slovakia, Slovenia,
Sweden, Taiwan, Thailand, Turkey, Ukraine, United Kingdom,
United States of America

### [Trang 5 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Algebra
Problem shortlist
52nd IMO 2011
Algebra
A1
A1
For any set A = {a1, a2, a3, a4} of four distinct positive integers with sum sA = a1 +a2+a3 +a4,
let pA denote the number of pairs (i, j) with 1 ≤i < j ≤4 for which ai + aj divides sA. Among
all sets of four distinct positive integers, determine those sets A for which pA is maximal.
A2
A2
Determine all sequences (x1, x2, . . . , x2011) of positive integers such that for every positive inte-
ger n there is an integer a with
xn
1 + 2xn
2 + · · · + 2011xn
2011 = an+1 + 1.
A3
A3
Determine all pairs (f, g) of functions from the set of real numbers to itself that satisfy
g(f(x + y)) = f(x) + (2x + y)g(y)
for all real numbers x and y.
A4
A4
Determine all pairs (f, g) of functions from the set of positive integers to itself that satisfy
f g(n)+1(n) + gf(n)(n) = f(n + 1) −g(n + 1) + 1
for every positive integer n. Here, f k(n) means f(f(. . . f
|
{z
}
k
(n) . . .)).
A5
A5
Prove that for every positive integer n, the set {2, 3, 4, . . . , 3n + 1} can be partitioned into
n triples in such a way that the numbers from each triple are the lengths of the sides of some
obtuse triangle.

### [Trang 6 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
52nd IMO 2011
Problem shortlist
Algebra
A6
A6
Let f be a function from the set of real numbers to itself that satisﬁes
f(x + y) ≤yf(x) + f(f(x))
for all real numbers x and y. Prove that f(x) = 0 for all x ≤0.
A7
A7
Let a, b, and c be positive real numbers satisfying min(a+b, b+c, c+a) >
√
2 and a2+b2+c2 = 3.
Prove that
a
(b + c −a)2 +
b
(c + a −b)2 +
c
(a + b −c)2 ≥
(abc)2.

### [Trang 7 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Combinatorics
Problem shortlist
52nd IMO 2011
Combinatorics
C1
C1
Let n > 0 be an integer. We are given a balance and n weights of weight 20, 21, . . . , 2n−1. In a
sequence of n moves we place all weights on the balance. In the ﬁrst move we choose a weight
and put it on the left pan. In each of the following moves we choose one of the remaining
weights and we add it either to the left or to the right pan. Compute the number of ways in
which we can perform these n moves in such a way that the right pan is never heavier than the
left pan.
C2
C2
Suppose that 1000 students are standing in a circle. Prove that there exists an integer k with
100 ≤k ≤300 such that in this circle there exists a contiguous group of 2k students, for which
the ﬁrst half contains the same number of girls as the second half.
C3
C3
Let S be a ﬁnite set of at least two points in the plane. Assume that no three points of S are
collinear. By a windmill we mean a process as follows. Start with a line ℓgoing through a
point P ∈S. Rotate ℓclockwise around the pivot P until the line contains another point Q
of S. The point Q now takes over as the new pivot. This process continues indeﬁnitely, with
the pivot always being a point from S.
Show that for a suitable P ∈S and a suitable starting line ℓcontaining P, the resulting
windmill will visit each point of S as a pivot inﬁnitely often.
C4
C4
Determine the greatest positive integer k that satisﬁes the following property: The set of positive
integers can be partitioned into k subsets A1, A2, . . . , Ak such that for all integers n ≥15 and
all i ∈{1, 2, . . . , k} there exist two distinct elements of Ai whose sum is n.

### [Trang 8 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
52nd IMO 2011
Problem shortlist
Combinatorics
C5
C5
Let m be a positive integer and consider a checkerboard consisting of m by m unit squares.
At the midpoints of some of these unit squares there is an ant. At time 0, each ant starts
moving with speed 1 parallel to some edge of the checkerboard. When two ants moving in
opposite directions meet, they both turn 90◦clockwise and continue moving with speed 1.
When more than two ants meet, or when two ants moving in perpendicular directions meet,
the ants continue moving in the same direction as before they met. When an ant reaches one
of the edges of the checkerboard, it falls oﬀand will not re-appear.
Considering all possible starting positions, determine the latest possible moment at which the
last ant falls oﬀthe checkerboard or prove that such a moment does not necessarily exist.
C6
C6
Let n be a positive integer and let W = . . . x−1x0x1x2 . . . be an inﬁnite periodic word consisting
of the letters a and b. Suppose that the minimal period N of W is greater than 2n.
A ﬁnite nonempty word U is said to appear in W if there exist indices k ≤ℓsuch that
U = xkxk+1 . . . xℓ. A ﬁnite word U is called ubiquitous if the four words Ua, Ub, aU, and bU
all appear in W. Prove that there are at least n ubiquitous ﬁnite nonempty words.
C7
C7
On a square table of 2011 by 2011 cells we place a ﬁnite number of napkins that each cover
a square of 52 by 52 cells. In each cell we write the number of napkins covering it, and we
record the maximal number k of cells that all contain the same nonzero number. Considering
all possible napkin conﬁgurations, what is the largest value of k?

### [Trang 9 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Geometry
Problem shortlist
52nd IMO 2011
Geometry
G1
G1
Let ABC be an acute triangle. Let ω be a circle whose center L lies on the side BC. Suppose
that ω is tangent to AB at B′ and to AC at C′. Suppose also that the circumcenter O of the
triangle ABC lies on the shorter arc B′C′ of ω. Prove that the circumcircle of ABC and ω
meet at two points.
G2
G2
Let A1A2A3A4 be a non-cyclic quadrilateral.
Let O1 and r1 be the circumcenter and the
circumradius of the triangle A2A3A4. Deﬁne O2, O3, O4 and r2, r3, r4 in a similar way. Prove
that
O1A2
1 −r2
+
O2A2
2 −r2
+
O3A2
3 −r2
+
O4A2
4 −r2
= 0.
G3
G3
Let ABCD be a convex quadrilateral whose sides AD and BC are not parallel. Suppose that the
circles with diameters AB and CD meet at points E and F inside the quadrilateral. Let ωE be
the circle through the feet of the perpendiculars from E to the lines AB, BC, and CD. Let ωF
be the circle through the feet of the perpendiculars from F to the lines CD, DA, and AB.
Prove that the midpoint of the segment EF lies on the line through the two intersection points
of ωE and ωF.
G4
G4
Let ABC be an acute triangle with circumcircle Ω. Let B0 be the midpoint of AC and let C0
be the midpoint of AB. Let D be the foot of the altitude from A, and let G be the centroid
of the triangle ABC. Let ω be a circle through B0 and C0 that is tangent to the circle Ωat a
point X̸ = A. Prove that the points D, G, and X are collinear.
G5
G5
Let ABC be a triangle with incenter I and circumcircle ω.
Let D and E be the second
intersection points of ω with the lines AI and BI, respectively. The chord DE meets AC at a
point F, and BC at a point G. Let P be the intersection point of the line through F parallel to
AD and the line through G parallel to BE. Suppose that the tangents to ω at A and at B meet
at a point K. Prove that the three lines AE, BD, and KP are either parallel or concurrent.

### [Trang 10 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
52nd IMO 2011
Problem shortlist
Geometry
G6
G6
Let ABC be a triangle with AB = AC, and let D be the midpoint of AC. The angle bisector
of ∠BAC intersects the circle through D, B, and C in a point E inside the triangle ABC.
The line BD intersects the circle through A, E, and B in two points B and F. The lines AF
and BE meet at a point I, and the lines CI and BD meet at a point K. Show that I is the
incenter of triangle KAB.
G7
G7
Let ABCDEF be a convex hexagon all of whose sides are tangent to a circle ω with center O.
Suppose that the circumcircle of triangle ACE is concentric with ω. Let J be the foot of the
perpendicular from B to CD. Suppose that the perpendicular from B to DF intersects the
line EO at a point K. Let L be the foot of the perpendicular from K to DE. Prove that
DJ = DL.
G8
G8
Let ABC be an acute triangle with circumcircle ω. Let t be a tangent line to ω. Let ta, tb,
and tc be the lines obtained by reﬂecting t in the lines BC, CA, and AB, respectively. Show
that the circumcircle of the triangle determined by the lines ta, tb, and tc is tangent to the
circle ω.

### [Trang 11 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Number Theory
Problem shortlist
52nd IMO 2011
Number Theory
N1
N1
For any integer d > 0, let f(d) be the smallest positive integer that has exactly d positive
divisors (so for example we have f(1) = 1, f(5) = 16, and f(6) = 12). Prove that for every
integer k ≥0 the number f(2k) divides f(2k+1).
N2
N2
Consider a polynomial P(x) = (x + d1)(x + d2) · . . . · (x + d9), where d1, d2, . . . , d9 are nine
distinct integers. Prove that there exists an integer N such that for all integers x ≥N the
number P(x) is divisible by a prime number greater than 20.
N3
N3
Let n ≥1 be an odd integer. Determine all functions f from the set of integers to itself such
that for all integers x and y the diﬀerence f(x) −f(y) divides xn −yn.
N4
N4
For each positive integer k, let t(k) be the largest odd divisor of k. Determine all positive
integers a for which there exists a positive integer n such that all the diﬀerences
t(n + a) −t(n),
t(n + a + 1) −t(n + 1),
. . . ,
t(n + 2a −1) −t(n + a −1)
are divisible by 4.
N5
N5
Let f be a function from the set of integers to the set of positive integers. Suppose that for
any two integers m and n, the diﬀerence f(m) −f(n) is divisible by f(m −n). Prove that for
all integers m, n with f(m) ≤f(n) the number f(n) is divisible by f(m).
N6
N6
Let P(x) and Q(x) be two polynomials with integer coeﬃcients such that no nonconstant
polynomial with rational coeﬃcients divides both P(x) and Q(x).
Suppose that for every
positive integer n the integers P(n) and Q(n) are positive, and 2Q(n) −1 divides 3P (n) −1.
Prove that Q(x) is a constant polynomial.

### [Trang 12 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
52nd IMO 2011
Problem shortlist
Number Theory
N7
N7
Let p be an odd prime number. For every integer a, deﬁne the number
Sa = a
1 + a2
2 + · · · + ap−1
p −1.
Let m and n be integers such that
S3 + S4 −3S2 = m
n .
Prove that p divides m.
N8
N8
Let k be a positive integer and set n = 2k + 1. Prove that n is a prime number if and only if
the following holds: there is a permutation a1, . . . , an−1 of the numbers 1, 2, . . . , n −1 and a
sequence of integers g1, g2, . . . , gn−1 such that n divides gai
i −ai+1 for every i ∈{1, 2, . . . , n−1},
where we set an = a1.

### [Trang 13 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
A1
Algebra – solutions
52nd IMO 2011
A1
For any set A = {a1, a2, a3, a4} of four distinct positive integers with sum sA = a1 +a2+a3 +a4,
let pA denote the number of pairs (i, j) with 1 ≤i < j ≤4 for which ai + aj divides sA. Among
all sets of four distinct positive integers, determine those sets A for which pA is maximal.
Answer.
The sets A for which pA is maximal are the sets the form {d, 5d, 7d, 11d} and
{d, 11d, 19d, 29d}, where d is any positive integer. For all these sets pA is 4.
Solution.
Firstly, we will prove that the maximum value of pA is at most 4. Without loss
of generality, we may assume that a1 < a2 < a3 < a4.
We observe that for each pair of
indices (i, j) with 1 ≤i < j ≤4, the sum ai + aj divides sA if and only if ai + aj divides
sA −(ai + aj) = ak + al, where k and l are the other two indices. Since there are 6 distinct
pairs, we have to prove that at least two of them do not satisfy the previous condition. We
claim that two such pairs are (a2, a4) and (a3, a4). Indeed, note that a2 + a4 > a1 + a3 and
a3 + a4 > a1 + a2. Hence a2 + a4 and a3 + a4 do not divide sA. This proves pA ≤4.
Now suppose pA = 4. By the previous argument we have
a1 + a4
 a2 + a3
and
a2 + a3
 a1 + a4,
a1 + a2
 a3 + a4
and
a3 + a4̸
 a1 + a2,
a1 + a3
 a2 + a4
and
a2 + a4̸
 a1 + a3.
Hence, there exist positive integers m and n with m > n ≥2 such that









a1 + a4 = a2 + a3
m(a1 + a2) = a3 + a4
n(a1 + a3) = a2 + a4.
Adding up the ﬁrst equation and the third one, we get n(a1 + a3) = 2a2 + a3 −a1. If n ≥3,
then n(a1 + a3) > 3a3 > 2a2 + a3 > 2a2 + a3 −a1. This is a contradiction. Therefore n = 2. If
we multiply by 2 the sum of the ﬁrst equation and the third one, we obtain
6a1 + 2a3 = 4a2,
while the sum of the ﬁrst one and the second one is
(m + 1)a1 + (m −1)a2 = 2a3.
Adding up the last two equations we get
(m + 7)a1 = (5 −m)a2.

### [Trang 14 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
52nd IMO 2011
Algebra – solutions
A1
It follows that 5 −m ≥1, because the left-hand side of the last equation and a2 are positive.
Since we have m > n = 2, the integer m can be equal only to either 3 or 4. Substituting
(3, 2) and (4, 2) for (m, n) and solving the previous system of equations, we ﬁnd the families of
solutions {d, 5d, 7d, 11d} and {d, 11d, 19d, 29d}, where d is any positive integer.

### [Trang 15 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
A2
Algebra – solutions
52nd IMO 2011
A2
Determine all sequences (x1, x2, . . . , x2011) of positive integers such that for every positive inte-
ger n there is an integer a with
xn
1 + 2xn
2 + · · · + 2011xn
2011 = an+1 + 1.
Answer.
The only sequence that satisﬁes the condition is
(x1, . . . , x2011) = (1, k, . . . , k)
with k = 2 + 3 + · · · + 2011 = 2023065.
Solution.
Throughout this solution, the set of positive integers will be denoted by Z+.
Put k = 2 + 3 + · · · + 2011 = 2023065. We have
1n + 2kn + · · · 2011kn = 1 + k · kn = kn+1 + 1
for all n, so (1, k, . . . , k) is a valid sequence. We shall prove that it is the only one.
Let a valid sequence (x1, . . . , x2011) be given. For each n ∈Z+ we have some yn ∈Z+ with
xn
1 + 2xn
2 + · · · + 2011xn
2011 = yn+1
n
+ 1.
Note that xn
1 + 2xn
2 + · · · + 2011xn
2011 < (x1 + 2x2 + · · · + 2011x2011)n+1, which implies that
the sequence (yn) is bounded. In particular, there is some y ∈Z+ with yn = y for inﬁnitely
many n.
Let m be the maximum of all the xi. Grouping terms with equal xi together, the sum xn
1 +
2xn
2 + · · · + 2011xn
2011 can be written as
xn
1 + 2xn
2 + · · · + xn
2011 = ammn + am−1(m −1)n + · · · + a1
with ai ≥0 for all i and a1 + · · · + am = 1 + 2 + · · · + 2011. So there exist arbitrarily large
values of n, for which
ammn + · · · + a1 −1 −y · yn = 0.
(1)
The following lemma will help us to determine the ai and y:
Lemma. Let integers b1, . . . , bN be given and assume that there are arbitrarily large positive
integers n with b1 + b22n + · · · + bNNn = 0. Then bi = 0 for all i.
Proof. Suppose that not all bi are zero. We may assume without loss of generality that bN̸ = 0.

### [Trang 16 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
52nd IMO 2011
Algebra – solutions
A2
Dividing through by Nn gives
|bN| =
bN−1
N −1
N
n
+ · · · + b1
 1
N
n ≤(|bN−1| + · · · + |b1|)
N −1
N
n
.
The expression
  N−1
N
n can be made arbitrarily small for n large enough, contradicting the
assumption that bN be non-zero.
□
We obviously have y > 1. Applying the lemma to (1) we see that am = y = m, a1 = 1,
and all the other ai are zero. This implies (x1, . . . , x2011) = (1, m, . . . , m). But we also have
1 + m = a1 + · · · + am = 1 + · · · + 2011 = 1 + k so m = k, which is what we wanted to show.


------------------------------------------------------------

## NGUỒN: IMO SHORTLIST OFFICIAL 2021-24 EN WITH SOLUTIONS
- **Phân hệ:** [HÌNH HỌC PHẲNG OLYMPIC 2D]
- **Tên file:** `IMO Shortlist Official 2021-24 EN with solutions.pdf` (371 trang)

### [Trang 1 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Shortlisted
Problems
(with solutions)
Conﬁdential until
1:30pm on 12 July 2022
(Norwegian time)
62nd International Mathematical Olympiad
Saint-Petersburg — Russia, 16th–24th July 2021

### [Trang 3 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Note of Conﬁdentiality
The Shortlist has to be kept strictly conﬁdential
until the conclusion of the following
International Mathematical Olympiad.
IMO General Regulations §6.6
Contributing Countries
The Organising Committee and the Problem Selection Committee of IMO 2021 thank the
following 51 countries for contributing 175 problem proposals:
Albania,
Algeria,
Armenia,
Australia,
Austria,
Azerbaijan,
Belgium,
Bangladesh, Canada, China, Colombia, Croatia, Czech Republic, Denmark,
Estonia, France, Germany, Greece, Hong Kong, Iceland, India, Iran,
Ireland,
Israel,
Japan,
Kazakhstan,
Kosovo,
Luxembourg,
Malaysia,
Mexico, Morocco, Myanmar, Netherlands, New Zealand, North Macedonia,
Poland, Romania, Singapore, Slovakia, Slovenia, South Africa, South Korea,
Spain, Switzerland, Taiwan, Thailand, U.S.A., Ukraine, United Kingdom,
Uzbekistan, Vietnam
Problem Selection Committee
Géza Kós, Gerhard Woeginger, Alexey Ustinov, Dmitry Krachun, Ivan Mitrofanov,
Sergey Berlov, Fedor Petrov, Ivan Frolov, Paul Vaderlind, Alexander Golovanov,
Ilya I. Bogdanov (chair)

### [Trang 5 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Shortlisted problems
Problems
Algebra
A1.
Let n be an integer, and let A be a subset of t0, 1, 2, 3, . . ., 5nu consisting of 4n ` 2
numbers. Prove that there exist a, b, c P A such that a ă b ă c and c ` 2a ą 3b.
A2.
For every integer n ě 1 consider the nˆn table with entry
Z
ij
n ` 1
^
at the intersection
of row i and column j, for every i “ 1, . . . , n and j “ 1, . . . , n. Determine all integers n ě 1 for
which the sum of the n2 entries in the table is equal to 1
4n2pn ´ 1q.
A3.
Given a positive integer n, ﬁnd the smallest value of
Ya1
]
`
Ya2
]
` ¨ ¨ ¨ `
Yan
n
]
over
all permutations pa1, a2, . . . , anq of p1, 2, . . . , nq.
A4.
Show that for all real numbers x1, . . . , xn the following inequality holds:
nÿ
i“1
nÿ
j“1
b
|xi ´ xj| ď
nÿ
i“1
nÿ
j“1
b
|xi ` xj|.
A5.
Let n ě 2 be an integer, and let a1, a2, . . . , an be positive real numbers such that
a1 ` a2 ` ¨ ¨ ¨ ` an “ 1. Prove that
nÿ
k“1
ak
1 ´ ak
pa1 ` a2 ` ¨ ¨ ¨ ` ak´1q2 ă 1
3.
A6.
Let A be a ﬁnite set of (not necessarily positive) integers, and let m ě 2 be an integer.
Assume that there exist non-empty subsets B1, B2, B3, . . . , Bm of A whose elements add up to
the sums m1, m2, m3, . . . , mm, respectively. Prove that A contains at least m{2 elements.
A7.
Let n ě 1 be an integer, and let x0, x1, . . . , xn`1 be n ` 2 non-negative real numbers
that satisfy xixi`1 ´ x2
i´1 ě 1 for all i “ 1, 2, . . . , n. Show that
x0 ` x1 ` ¨ ¨ ¨ ` xn ` xn`1 ą
ˆ2n
˙3{2
.
A8.
Determine all functions f : R Ñ R that satisfy
`
fpaq ´ fpbq
˘ `
fpbq ´ fpcq
˘ `
fpcq ´ fpaq
˘
“ fpab2 ` bc2 ` ca2q ´ fpa2b ` b2c ` c2aq
for all real numbers a, b, c.

### [Trang 6 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
6
Saint-Petersburg — Russia, 16th–24th July 2021
Combinatorics
C1.
Let S be an inﬁnite set of positive integers, such that there exist four pairwise distinct
a, b, c, d P S with gcdpa, bq ‰ gcdpc, dq. Prove that there exist three pairwise distinct x, y, z P S
such that gcdpx, yq “ gcdpy, zq ‰ gcdpz, xq.
C2.
Let n ě 3 be an integer. An integer m ě n ` 1 is called n-colourful if, given inﬁnitely
many marbles in each of n colours C1, C2, . . . , Cn, it is possible to place m of them around a
circle so that in any group of n ` 1 consecutive marbles there is at least one marble of colour
Ci for each i “ 1, . . . , n.
Prove that there are only ﬁnitely many positive integers which are not n-colourful. Find
the largest among them.
C3.
A thimblerigger has 2021 thimbles numbered from 1 through 2021. The thimbles are
arranged in a circle in arbitrary order. The thimblerigger performs a sequence of 2021 moves;
in the kth move, he swaps the positions of the two thimbles adjacent to thimble k.
Prove that there exists a value of k such that, in the kth move, the thimblerigger swaps
some thimbles a and b such that a ă k ă b.
C4.
The kingdom of Anisotropy consists of n cities. For every two cities there exists exactly
one direct one-way road between them. We say that a path from X to Y is a sequence of roads
such that one can move from X to Y along this sequence without returning to an already
visited city. A collection of paths is called diverse if no road belongs to two or more paths in
the collection.
Let A and B be two distinct cities in Anisotropy. Let NAB denote the maximal number of
paths in a diverse collection of paths from A to B. Similarly, let NBA denote the maximal num-
ber of paths in a diverse collection of paths from B to A. Prove that the equality NAB “ NBA
holds if and only if the number of roads going out from A is the same as the number of roads
going out from B.
C5.
Let n and k be two integers with n ą k ě 1. There are 2n ` 1 students standing in
a circle. Each student S has 2k neighbours— namely, the k students closest to S on the right,
and the k students closest to S on the left.
Suppose that n ` 1 of the students are girls, and the other n are boys. Prove that there is
a girl with at least k girls among her neighbours.
C6.
A hunter and an invisible rabbit play a game on an inﬁnite square grid. First the
hunter ﬁxes a colouring of the cells with ﬁnitely many colours. The rabbit then secretly chooses
a cell to start in. Every minute, the rabbit reports the colour of its current cell to the hunter,
and then secretly moves to an adjacent cell that it has not visited before (two cells are adjacent
if they share a side). The hunter wins if after some ﬁnite time either
• the rabbit cannot move; or
• the hunter can determine the cell in which the rabbit started.
Decide whether there exists a winning strategy for the hunter.

### [Trang 7 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Shortlisted problems
C7.
Consider a checkered 3m ˆ 3m square, where m is an integer greater than 1. A frog
sits on the lower left corner cell S and wants to get to the upper right corner cell F. The frog
can hop from any cell to either the next cell to the right or the next cell upwards.
Some cells can be sticky, and the frog gets trapped once it hops on such a cell. A set X of
cells is called blocking if the frog cannot reach F from S when all the cells of X are sticky. A
blocking set is minimal if it does not contain a smaller blocking set.
(a) Prove that there exists a minimal blocking set containing at least 3m2 ´ 3m cells.
(b) Prove that every minimal blocking set contains at most 3m2 cells.
Note. An example of a minimal blocking set for m “ 2 is shown below. Cells of the set X are marked
by letters x.
S
F
x
x
x
x
x
x
C8.
Determine the largest N for which there exists a table T of integers with N rows and
100 columns that has the following properties:
(i) Every row contains the numbers 1, 2, . . . , 100 in some order.
(ii) For any two distinct rows r and s, there is a column c such that |Tpr, cq ´ Tps, cq| ě 2.
Here Tpr, cq means the number at the intersection of the row r and the column c.

### [Trang 8 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
8
Saint-Petersburg — Russia, 16th–24th July 2021
Geometry
G1.
Let ABCD be a parallelogram such that AC “ BC. A point P is chosen on the
extension of the segment AB beyond B.
The circumcircle of the triangle ACD meets the
segment PD again at Q, and the circumcircle of the triangle APQ meets the segment PC
again at R. Prove that the lines CD, AQ, and BR are concurrent.
G2.
Let ABCD be a convex quadrilateral circumscribed around a circle with centre I.
Let ω be the circumcircle of the triangle ACI. The extensions of BA and BC beyond A and
C meet ω at X and Z, respectively. The extensions of AD and CD beyond D meet ω at Y
and T, respectively. Prove that the perimeters of the (possibly self-intersecting) quadrilaterals
ADTX and CDY Z are equal.
G3.
Version 1.
Let n be a ﬁxed positive integer, and let S be the set of points px, yq on the
Cartesian plane such that both coordinates x and y are nonnegative integers smaller than 2n
(thus |S| “ 4n2). Assume that F is a set consisting of n2 quadrilaterals such that all their
vertices lie in S, and each point in S is a vertex of exactly one of the quadrilaterals in F.
Determine the largest possible sum of areas of all n2 quadrilaterals in F.
Version 2.
Let n be a ﬁxed positive integer, and let S be the set of points px, yq on the
Cartesian plane such that both coordinates x and y are nonnegative integers smaller than 2n
(thus |S| “ 4n2). Assume that F is a set of polygons such that all vertices of polygons in F lie
in S, and each point in S is a vertex of exactly one of the polygons in F.
Determine the largest possible sum of areas of all polygons in F.
G4.
Let ABCD be a quadrilateral inscribed in a circle Ω. Let the tangent to Ωat D
intersect the rays BA and BC at points E and F, respectively. A point T is chosen inside the
triangle ABC so that TE ∥CD and TF ∥AD. Let K ‰ D be a point on the segment DF
such that TD “ TK. Prove that the lines AC, DT and BK intersect at one point.
G5.
Let ABCD be a cyclic quadrilateral whose sides have pairwise diﬀerent lengths. Let
O be the circumcentre of ABCD. The internal angle bisectors of =ABC and =ADC meet AC
at B1 and D1, respectively. Let OB be the centre of the circle which passes through B and is
tangent to AC at D1. Similarly, let OD be the centre of the circle which passes through D and
is tangent to AC at B1.
Assume that BD1 ∥DB1. Prove that O lies on the line OBOD.
G6.
Determine all integers n ě 3 satisfying the following property: every convex n-gon
whose sides all have length 1 contains an equilateral triangle of side length 1.
(Every polygon is assumed to contain its boundary.)

### [Trang 9 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Shortlisted problems
G7.
A point D is chosen inside an acute-angled triangle ABC with AB ą AC so that
=BAD “ =DAC. A point E is constructed on the segment AC so that =ADE “ =DCB.
Similarly, a point F is constructed on the segment AB so that =ADF “ =DBC. A point
X is chosen on the line AC so that CX “ BX. Let O1 and O2 be the circumcentres of the
triangles ADC and DXE. Prove that the lines BC, EF, and O1O2 are concurrent.
G8.
Let ω be the circumcircle of a triangle ABC, and let ΩA be its excircle which is tangent
to the segment BC. Let X and Y be the intersection points of ω and ΩA. Let P and Q be the
projections of A onto the tangent lines to ΩA at X and Y , respectively. The tangent line at P
to the circumcircle of the triangle APX intersects the tangent line at Q to the circumcircle of
the triangle AQY at a point R. Prove that AR K BC.

### [Trang 10 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
10
Saint-Petersburg — Russia, 16th–24th July 2021
Number Theory
N1.
Determine all integers n ě 1 for which there exists a pair of positive integers pa, bq
such that no cube of a prime divides a2 ` b ` 3 and
ab ` 3b ` 8
a2 ` b ` 3 “ n.
N2.
Let n ě 100 be an integer. The numbers n, n ` 1, . . . , 2n are written on n ` 1 cards,
one number per card. The cards are shuﬄed and divided into two piles. Prove that one of the
piles contains two cards such that the sum of their numbers is a perfect square.
N3.
Find all positive integers n with the following property: the k positive divisors of n
have a permutation pd1, d2, . . . , dkq such that for every i “ 1, 2, . . . , k, the number d1 ` ¨ ¨ ¨ ` di
is a perfect square.
N4.
Alice is given a rational number r ą 1 and a line with two points B ‰ R, where
point R contains a red bead and point B contains a blue bead. Alice plays a solitaire game by
performing a sequence of moves. In every move, she chooses a (not necessarily positive) integer
k, and a bead to move. If that bead is placed at point X, and the other bead is placed at Y ,
then Alice moves the chosen bead to point X1 with ÝÝÑ
Y X1 “ rk ÝÝÑ
Y X.
Alice’s goal is to move the red bead to the point B. Find all rational numbers r ą 1 such
that Alice can reach her goal in at most 2021 moves.
N5.
Prove that there are only ﬁnitely many quadruples pa, b, c, nq of positive integers such
that
n! “ an´1 ` bn´1 ` cn´1.
N6.
Determine all integers n ě 2 with the following property: every n pairwise distinct
integers whose sum is not divisible by n can be arranged in some order a1, a2, . . . , an so that
n divides 1 ¨ a1 ` 2 ¨ a2 ` ¨ ¨ ¨ ` n ¨ an.
N7.
Let a1, a2, a3, . . . be an inﬁnite sequence of positive integers such that an`2m divides
an ` an`m for all positive integers n and m. Prove that this sequence is eventually periodic, i.e.
there exist positive integers N and d such that an “ an`d for all n ą N.
N8.
For a polynomial Ppxq with integer coeﬃcients let P 1pxq “ Ppxq and P k`1pxq “
PpP kpxqq for k ě 1. Find all positive integers n for which there exists a polynomial Ppxq with
integer coeﬃcients such that for every integer m ě 1, the numbers P mp1q, . . . , P mpnq leave
exactly rn{2ms distinct remainders when divided by n.

### [Trang 13 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Shortlisted problems – solutions
Solutions
Algebra
A1.
Let n be an integer, and let A be a subset of t0, 1, 2, 3, . . ., 5nu consisting of 4n ` 2
numbers. Prove that there exist a, b, c P A such that a ă b ă c and c ` 2a ą 3b.
Solution 1.
(By contradiction) Suppose that there exist 4n ` 2 non-negative integers x0 ă
x1 ă ¨ ¨ ¨ ă x4n`1 that violate the problem statement. Then in particular x4n`1 ` 2xi ď 3xi`1
for all i “ 0, . . . , 4n ´ 1, which gives
x4n`1 ´ xi ě 3
2px4n`1 ´ xi`1q.
By a trivial induction we then get
x4n`1 ´ xi ě
ˆ3
˙4n´i
px4n`1 ´ x4nq,
which for i “ 0 yields the contradiction
x4n`1 ´ x0 ě
ˆ3
˙4n
px4n`1 ´ x4nq “
ˆ81
˙n
px4n`1 ´ x4nq ą 5n ¨ 1.
Solution 2. Denote the maximum element of A by c. For k “ 0, . . . , 4n ´ 1 let
Ak “
␣
x P A : p1 ´ p2{3qkqc ď x ă p1 ´ p2{3qk`1qc
(
.
Note that
p1 ´ p2{3q4nqc “ c ´ p16{81qnc ą c ´ p1{5qnc ě c ´ 1,
which shows that the sets A0, A1, . . . , A4n´1 form a partition of Aztcu. Since Aztcu has 4n` 1
elements, by the pigeonhole principle some set Ak does contain at least two elements of Aztcu.
Denote these two elements a and b and assume a ă b, so that a ă b ă c. Then
c ` 2a ě c ` 2p1 ´ p2{3qkqc “ p3 ´ 2p2{3qkqc “ 3p1 ´ p2{3qk`1qc ą 3b,
as desired.

### [Trang 14 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
14
Saint-Petersburg — Russia, 16th–24th July 2021
A2.
For every integer n ě 1 consider the nˆn table with entry
Z
ij
n ` 1
^
at the intersection
of row i and column j, for every i “ 1, . . . , n and j “ 1, . . . , n. Determine all integers n ě 1 for
which the sum of the n2 entries in the table is equal to 1
4n2pn ´ 1q.
Answer: All integers n for which n ` 1 is a prime.
Solution 1.
First, observe that every pair x, y of real numbers for which the sum x ` y is
integer satisﬁes
txu ` tyu ě x ` y ´ 1.
(1)
The inequality is strict if x and y are integers, and it holds with equality otherwise.
We estimate the sum S as follows.
2S “
ÿ
1ďi,jďn
ˆZ
ij
n ` 1
^
`
Z
ij
n ` 1
^˙
“
ÿ
1ďi,jďn
ˆZ
ij
n ` 1
^
`
Zpn ` 1 ´ iqj
n ` 1
^˙
ě
ÿ
1ďi,jďn
pj ´ 1q “ pn ´ 1qn2
.
The inequality in the last line follows from (1) by setting x “ ij{pn ` 1q and y “ pn ` 1 ´
iqj{pn ` 1q, so that x ` y “ j is integral.
Now S “ 1
4n2pn ´ 1q if and only if the inequality in the last line holds with equality, which
means that none of the values ij{pn ` 1q with 1 ď i, j ď n may be integral.
Hence, if n ` 1 is composite with factorisation n ` 1 “ ab for 2 ď a, b ď n, one gets a
strict inequality for i “ a and j “ b. If n ` 1 is a prime, then ij{pn ` 1q is never integral and
S “ 1
4n2pn ´ 1q.
Solution 2.
To simplify the calculation with indices, extend the table by adding a phantom
column of index 0 with zero entries (which will not change the sum of the table). Fix a row i
with 1 ď i ď n, and let d :“ gcdpi, n ` 1q and k :“ pn ` 1q{d. For columns j “ 0, . . . , n, deﬁne
the remainder rj :“ ij mod pn ` 1q. We ﬁrst prove the following
Claim. For every integer g with 1 ď g ď d, the remainders rj with indices j in the range
pg ´ 1qk ď j ď gk ´ 1
(2)
form a permutation of the k numbers 0 ¨ d, 1 ¨ d, 2 ¨ d, . . . , pk ´ 1q ¨ d.
Proof. If rj1 “ rj holds for two indices j1 and j in (2), then ipj1´jq ” 0 mod pn ` 1q, so that j1´j
is a multiple of k; since |j1´j| ď k´1, this implies j1 “ j. Hence, the k remainders are pairwise
distinct. Moreover, each remainder rj “ ij mod pn ` 1q is a multiple of d “ gcdpi, n ` 1q. This
proves the claim.
We then have
nÿ
j“0
rj “
dÿ
g“1
pn`1q{d´1
ÿ
ℓ“0
ℓd “ d2 ¨ 1
ˆn ` 1
d
´ 1
˙ n ` 1
d
“ pn ` 1 ´ dqpn ` 1q
.
(3)
By using (3), compute the sum Si of row i as follows:
Si “
nÿ
j“0
Z
ij
n ` 1
^
“
nÿ
j“0
ij ´ rj
n ` 1 “
i
n ` 1
nÿ
j“0
j ´
n ` 1
nÿ
j“0
rj
“
i
n ` 1 ¨ npn ` 1q
´
n ` 1 ¨ pn ` 1 ´ dqpn ` 1q
“ pin ´ n ´ 1 ` dq
.
(4)

### [Trang 15 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Shortlisted problems – solutions
Equation (4) yields the following lower bound on the row sum Si, which holds with equality if
and only if d “ gcdpi, n ` 1q “ 1:
Si ě pin ´ n ´ 1 ` 1q
“ npi ´ 1q
.
(5)
By summing up the bounds (5) for the rows i “ 1, . . . , n, we get the following lower bound for
the sum of all entries in the table
nÿ
i“1
Si ě
nÿ
i“1
n
2pi ´ 1q “ n2pn ´ 1q
.
(6)
In (6) we have equality if and only if equality holds in (5) for each i “ 1, . . . , n, which happens
if and only if gcdpi, n ` 1q “ 1 for each i “ 1, . . . , n, which is equivalent to the fact that n ` 1
is a prime. Thus the sum of the table entries is 1
4n2pn ´ 1q if and only if n ` 1 is a prime.
Comment. To simplify the answer, in the problem statement one can make a change of variables by
introducing m :“ n ` 1 and writing everything in terms of m. The drawback is that the expression for
the sum will then be 1
4pm ´ 1q2pm ´ 2q which seems more artiﬁcial.

### [Trang 16 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
16
Saint-Petersburg — Russia, 16th–24th July 2021
A3.
Given a positive integer n, ﬁnd the smallest value of
Ya1
]
`
Ya2
]
` ¨ ¨ ¨ `
Yan
n
]
over
all permutations pa1, a2, . . . , anq of p1, 2, . . . , nq.
Answer: The minimum of such sums is tlog2 nu ` 1; so if 2k ď n ă 2k`1, the minimum is k ` 1.
Solution 1.
Suppose that 2k ď n ă 2k`1 with some nonnegative integer k. First we show a
permutation pa1, a2, . . . , anq such that
X a1
\
`
X a2
\
` ¨ ¨ ¨ `
X an
n
\
“ k ` 1; then we will prove that
X a1
\
`
X a2
\
` ¨ ¨ ¨ `
X an
n
\
ě k ` 1 for every permutation. Hence, the minimal possible value will
be k ` 1.
I. Consider the permutation
pa1q “ p1q,
pa2, a3q “ p3, 2q,
pa4, a5, a6, a7q “ p7, 4, 5, 6q,
. . .
pa2k´1, . . . , a2k´1q “ p2k ´ 1, 2k´1, 2k´1 ` 1, . . . , 2k ´ 2q,
pa2k, . . . , anq “ pn, 2k, 2k ` 1, . . . , n ´ 1q.
This permutation consists of k ` 1 cycles. In every cycle pap, . . . , aqq “ pq, p, p ` 1, . . . , q ´ 1q
we have q ă 2p, so
qÿ
i“p
Zai
i
^
“
Zq
p
^
`
qÿ
i“p`1
Zi ´ 1
i
^
“ 1;
The total sum over all cycles is precisely k ` 1.
II. In order to establish the lower bound, we prove a more general statement.
Claim. If b1, . . . , b2k are distinct positive integers then
2k
ÿ
i“1
Zbi
i
^
ě k ` 1.
From the Claim it follows immediately that
nÿ
i“1
Yai
i
]
ě
2k
ÿ
i“1
Yai
i
]
ě k ` 1.
Proof of the Claim.
Apply induction on k. For k “ 1 the claim is trivial,
X b1
\
ě 1. Suppose
the Claim holds true for some positive integer k, and consider k ` 1.
If there exists an index j such that 2k ă j ď 2k`1 and bj ě j then
2k`1
ÿ
i“1
Zbi
i
^
ě
2k
ÿ
i“1
Zbi
i
^
`
Zbj
j
^
ě pk ` 1q ` 1
by the induction hypothesis, so the Claim is satisﬁed.
Otherwise we have bj ă j ď 2k`1 for every 2k ă j ď 2k`1. Among the 2k`1 distinct numbers
b1, . . . , b2k`1 there is some bm which is at least 2k`1; that number must be among b1 . . . , b2k.
Hence, 1 ď m ď 2k and bm ě 2k`1.
We will apply the induction hypothesis to the numbers
c1 “ b1, . . . , cm´1 “ bm´1,
cm “ b2k`1,
cm`1 “ bm`1, . . . , c2k “ b2k,
so take the ﬁrst 2k numbers but replace bm with b2k`1. Notice that
Zbm
m
^
ě
Z2k`1
m
^
“
Z2k ` 2k
m
^
ě
Zb2k`1 ` m
m
^
“
Zcm
m
^
` 1.

### [Trang 17 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Shortlisted problems – solutions
For the other indices i with 1 ď i ď 2k, i ‰ m we have
X bi
i
\
“
X ci
i
\
, so
2k`1
ÿ
i“1
Zbi
i
^
“
2k
ÿ
i“1
Zbi
i
^
ě
2k
ÿ
i“1
Zci
i
^
` 1 ě pk ` 1q ` 1.
That proves the Claim and hence completes the solution.
l
Solution 2. We present a diﬀerent proof for the lower bound.
Assume again 2k ď n ă 2k`1, and let P “ t20, 21, . . . , 2ku be the set of powers of 2 among
1, 2, . . . , n. Call an integer i P t1, 2, . . . , nu and the interval ri, ais good if ai ě i.
Lemma 1. The good intervals cover the integers 1, 2, . . . , n.
Proof. Consider an arbitrary x P t1, 2 . . . , nu; we want to ﬁnd a good interval ri, ais that covers x;
i.e., i ď x ď ai. Take the cycle of the permutation that contains x, that is px, ax, aax, . . .q. In
this cycle, let i be the ﬁrst element with ai ě x; then i ď x ď ai.
l
Lemma 2. If a good interval ri, ais covers p distinct powers of 2 then
X ai
i
\
ě p; more formally,
X ai
i
\
ě
ˇˇri, ais X P
ˇˇ.
Proof. The ratio of the smallest and largest powers of 2 in the interval is at least 2p´1. By
Bernoulli’s inequality, ai
i ě 2p´1 ě p; that proves the lemma.
l
Now, by Lemma 1, the good intervals cover P. By applying Lemma 2 as well, we obtain
that
nÿ
i“1
Zai
i
^
“
nÿ
i is good
Zai
i
^
ě
nÿ
i is good
ˇˇˇri, ais X P
ˇˇˇ ě
ˇˇP
ˇˇ “ k ` 1.
Solution 3. We show yet another proof for the lower bound, based on the following inequality.
Lemma 3.
Za
b
^
ě log2
a ` 1
b
for every pair a, b of positive integers.
Proof. Let t “
X a
b
\
, so t ď a
b and a`1
b
ď t ` 1. By applying the inequality 2t ě t ` 1, we obtain
Za
b
^
“ t ě log2pt ` 1q ě log2
a ` 1
b
.
l
By applying the lemma to each term, we get
nÿ
i“1
Zai
i
^
ě
nÿ
i“1
log2
ai ` 1
i
“
nÿ
i“1
log2pai ` 1q ´
nÿ
i“1
log2 i.
Notice that the numbers a1 ` 1, a2 ` 1, . . . , an ` 1 form a permutation of 2, 3, . . . , n ` 1. Hence,
in the last two sums all terms cancel out, except for log2pn ` 1q in the ﬁrst sum and log2 1 “ 0
in the second sum. Therefore,
nÿ
i“1
Zai
i
^
ě log2pn ` 1q ą k.
As the left-hand side is an integer, it must be at least k ` 1.

### [Trang 18 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
18
Saint-Petersburg — Russia, 16th–24th July 2021
A4.
Show that for all real numbers x1, . . . , xn the following inequality holds:
nÿ
i“1
nÿ
j“1
b
|xi ´ xj| ď
nÿ
i“1
nÿ
j“1
b
|xi ` xj|.
Solution 1. If we add t to all the variables then the left-hand side remains constant and the
right-hand side becomes
Hptq :“
nÿ
i“1
nÿ
j“1
b
|xi ` xj ` 2t|.
Let T be large enough such that both Hp´Tq and HpTq are larger than the value L of the left-
hand side of the inequality we want to prove. Not necessarily distinct points pi,j :“ ´pxi`xjq{2
together with T and ´T split the real line into segments and two rays such that on each of
these segments and rays the function Hptq is concave since fptq :“
a
|ℓ` 2t| is concave on
both intervals p´8, ´ℓ{2s and r´ℓ{2, `8q. Let ra, bs be the segment containing zero. Then
concavity implies Hp0q ě mintHpaq, Hpbqu and, since Hp˘Tq ą L, it suﬃces to prove the
inequalities Hp´pxi ` xjq{2q ě L, that is to prove the original inequality in the case when all
numbers are shifted in such a way that two variables xi and xj add up to zero. In the following
we denote the shifted variables still by xi.
If i “ j, i.e. xi “ 0 for some index i, then we can remove xi which will decrease both sides
by 2 ř
k
a
|xk|. Similarly, if xi `xj “ 0 for distinct i and j we can remove both xi and xj which
decreases both sides by
a
2|xi| ` 2 ¨
ÿ
k‰i,j
ˆa
|xk ` xi| `
b
|xk ` xj|
˙
.
In either case we reduced our inequality to the case of smaller n. It remains to note that for
n “ 0 and n “ 1 the inequality is trivial.
Solution 2. For real p consider the integral
Ippq “
ż 8
1 ´ cosppxq
x?x
dx,
which clearly converges to a strictly positive number. By changing the variable y “ |p|x one
notices that Ippq “
a
|p|Ip1q. Hence, by using the trigonometric formula cospα ´ βq ´ cospα `
βq “ 2 sin α sin β we obtain
a
|a ` b|´
a
|a ´ b| “
Ip1q
ż 8
cosppa ´ bqxq ´ cosppa ` bqxq
x?x
dx “
Ip1q
ż 8
2 sinpaxq sinpbxq
x?x
dx,
from which our inequality immediately follows:
nÿ
i“1
nÿ
j“1
b
|xi ` xj| ´
nÿ
i“1
nÿ
j“1
b
|xi ´ xj| “
Ip1q
ż 8
`řn
i“1 sinpxixq
˘2
x?x
dx ě 0.
Comment 1. A more general inequality
nÿ
i“1
nÿ
j“1
|xi ´ xj|r ď
nÿ
i“1
nÿ
j“1
|xi ` xj|r
holds for any r P r0, 2s. The ﬁrst solution can be repeated verbatim for any r P r0, 1s but not for r ą 1.
In the second solution, by putting xr`1 in the denominator in place of x?x we can prove the inequality
for any r P p0, 2q and the cases r “ 0, 2 are easy to check by hand.
Comment 2. In fact, the integral from Solution 2 can be computed explicitly, we have Ip1q “
?
2π.

### [Trang 19 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Shortlisted problems – solutions
A5.
Let n ě 2 be an integer, and let a1, a2, . . . , an be positive real numbers such that
a1 ` a2 ` ¨ ¨ ¨ ` an “ 1. Prove that
nÿ
k“1
ak
1 ´ ak
pa1 ` a2 ` ¨ ¨ ¨ ` ak´1q2 ă 1
3.
Solution 1. For all k ď n, let
sk “ a1 ` a2 ` ¨ ¨ ¨ ` ak
and
bk “ aks2
k´1
1 ´ ak
,
with the convention that s0 “ 0. Note that bk is exactly a summand in the sum we need to
estimate. We shall prove the inequality
bk ă s3
k ´ s3
k´1
.
(1)
Indeed, it suﬃces to check that
(1) ðñ 0 ă p1 ´ akq
`
psk´1 ` akq3 ´ s3
k´1
˘
´ 3aks2
k´1
ðñ 0 ă p1 ´ akq
`
3s2
k´1 ` 3sk´1ak ` a2
k
˘
´ 3s2
k´1
ðñ 0 ă ´3aks2
k´1 ` 3p1 ´ akqsk´1ak ` p1 ´ akqa2
k
ðñ 0 ă 3p1 ´ ak ´ sk´1qsk´1ak ` p1 ´ akqa2
k
which holds since ak ` sk´1 “ sk ď 1 and ak P p0, 1q.
Thus, adding inequalities (1) for k “ 1, . . . , n, we conclude that
b1 ` b2 ` ¨ ¨ ¨ ` bn ă s3
n ´ s3
3
“ 1
3,
as desired.
Comment 1. There are many ways of proving (1) which can be written as
as2
1 ´ a ´ pa ` sq3 ´ s3
ă 0,
(2)
for non-negative a and s satisfying a ` s ď 1 and a ą 0.
E.g., note that for any ﬁxed a the expression in (2) is quadratic in s with the leading coeﬃcient
a{p1 ´ aq ´ a ą 0. Hence, it is convex as a function in s, so it suﬃces to check the inequality at s “ 0
and s “ 1 ´ a. The former case is trivial and in the latter case the inequality can be rewritten as
as ´ 3aspa ` sq ` a3
ă 0,
which is trivial since a ` s “ 1.
Solution 2. First, let us deﬁne
Spa1, . . . , anq :“
nÿ
k“1
ak
1 ´ ak
pa1 ` a2 ` ¨ ¨ ¨ ` ak´1q2.


------------------------------------------------------------

## NGUỒN: SHARYGIN GEOMETRY OLYMPIAD 2005-25 EN WITH SOLUTIONS
- **Phân hệ:** [HÌNH HỌC PHẲNG OLYMPIC 2D]
- **Tên file:** `Sharygin Geometry Olympiad 2005-25 EN with solutions.pdf` (877 trang)

### [Trang 1 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
The rst Olympiad, 2005
Correspondence round
1. [8] The circle chords AC and BD intersect at point P. Perpendiculars to AC and BD
at points C and D respectively intersect at point Q. Prove that the lines AB and PQ are
perpendicular.
2. [8,9] Cut the cross composed of ve equal squares into three polygons of equal area and
perimeter.
3. [8,9] A circle and a point K inside it are given. An arbitrary circle of the same size passes
through point K and shares a chord with the initial circle. Find the locus of midpoints of such
chords.
4. [9-11] For what minimal n there exists a convex n-gon with equal sines of all angles and
unequal lengths of all sides?
5. [8-10] Two parallel lines p1 and p2 are given. Points A and B belong to p1, point C belongs
to p2. We move the segment BC parallel to itself and consider all triangles ABC produced in
this manner. In these triangles, nd the locus of points that are: a) intersections of altitudes;
b) intersections of medians; c) circumcenters.
6. [10,11] The side AB of the triangle ABC has been divided into n equal parts (with points
of division B0 = A, B1, B2, . . . , Bn = B), while the side AC of this triangle has been divided
into (n + 1) equal parts (with points of division C0 = A, C1, C2, . . . , Cn+1 = C). Triangles
CiBiCi+1 were colored. What part of the triangle area has been colored?
7. [8,9] Two circles with radii of 1 and 2 have common center at point O. Vertex A of the
regular triangle ABC is on the major circle, whereas the midpoint of BC is on the minor circle.
What is the possible measure of angle BOC?
8. [8,9] Three rectangles are circumscribed about a convex quadrilateral ABCD. Two of
these rectangles are squares. Is it true that the third rectangle has to be a square as well? (A
rectangle is circumscribed about a quadrilateral ABCD when there is a single vertex of the
quadrilateral on each side of the rectangle).
9. [9] Let O be the center of a regular triangle ABC. From arbitrary point P on the plane
the perpendiculars were dropped to the sides of the triangle or their extensions. Let M be the
intersection of medians of the triangle with vertices in the feet of the perpendiculars. Prove
that M is a midpoint of segment PO.
10. [8,9] Cut a non-isosceles triangle into four similar triangles not all of which are congruent.
11. [8-10] A square has been cut into n rectangles with sides equal to ai × bi, i = 1, . . . , n.
At what minimal n all numbers in the tuple a1, . . . , an, b1 . . . , bn can occur to be dierent?
12. [8,9] Construct a quadrilateral with the given sides a, b, c and d and the distance l
between the midpoints of the diagonals.
13. [9] A triangle ABC and two lines l1 and l2 are given. A line parallel to l1 and intersecting
AC at point E, as well as a line parallel to l2 and intersecting BC at point F are both drawn
through an arbitrary point D. Construct the point D such that the segment EF has minimal
length.
14. [10,11] Let P be an arbitrary point inside triangle ABC. Denote by A1, B1 and C1 the
points of intersection of lines AP, BP and CP with sides BC, CA and AB respectively. Rank
areas of the triangles AB1C1,A1BC1, A1B1C and denote the smallest as S1, the middle one as
S2, and the largest one as S3. Prove that √S1S2 ≤S ≤√S2S3 , where S is the area of triangle
A1B1C1.

### [Trang 2 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
15. [11] A circle with its center at the origin is given. Prove that there exists a circle with a
shorter radius, which contains equal or greater number of points with integer coordinates.
16. [8,9] In an acute non-regular triangle 4 points were marked: the centers of the incircle and
the circumcircle, the center of mass (the intersection point of the medians) and the orthocenter
(the intersection point of the altitudes). After that, the original triangle was erased. It turned
out to be impossible to determine which point corresponded to which center. Find the angles
of the triangle.
17. [11] The incircle of triangle ABC has center I and tangency points P, Q, R with sides
BC, CA and AB respectively. With a ruler only, construct the point K where the circle passing
through B and C is (internally) tangent with the incircle.
18. [10,11] There are three lines l1, l2, l3 in the plane that form a triangle, as well as a
marked point O, the center of its circumcircle. For an arbitrary point X in the plane, let us
denote by Xi the point symmetrical to about the line li.
a) Prove that for an arbitrary point M the lines linking midpoints of segments O1O2 and
M1M2, O2O3 and M2M3, O3O1 and M3M1 concur.
b) Where can their point of intersection lie?
19. [8-11] As is well-known, the Moon rotates around the Earth. Let us assume the Moon
and the Earth to be points. Assume also that the Moon travels a circular orbit around the
Earth and makes full circle in one month. There is an UFO in the plane of the lunar orbit. The
UFO can move in jumps over the Moon and over the Earth: from an old location (point A) it
instantly moves to the new one (point A′) so that the midpoint of A′ is either the Moon, or the
Earth. Between the jumps, the UFO is located in space motionless.
a) Determine the minimal number of jumps sucient for the UFO to reach any random
point within lunar orbit from any another random point within lunar orbit.
b) Prove that the UFO is able, within innite number of jumps, to reach any random point
within lunar orbit from any another random point within lunar orbit in any period of time, for
example, in one second.
20. [11] Let I be the center of the insphere of tetrahedron ABCD; A′, B′, C′, D′ be the
centers of the circumspheres of tetrahedrons IBCD, ICDA, IDBA, IABC respectively. Prove
that the circumsphere of ABCD lies entirely inside the circumsphere of A′B′C′D′.
21. [10,11] The planet Tetraincognito covered by the ocean has a shape of a regular
tetrahedron with an edge of 900 kilometers. What area of the ocean will be hit by a tsunami
after 2 hours of tetraquake with the epicenter at
a) the center of a face,
b) the midpoint of an edge, if tsunami propagates at a speed of 300 km/h?
22. [10,11] Perpendiculars were dropped to the faces of a tetrahedron at their mass centers
(intersections of medians). Prove that the projections of three perpendiculars onto the fourth
face concur.
23. [10,11] Paste over a cube in one layer with ve convex pentagons of equal area.
24. [10,11] Given a triangle with all its angles less than φ, where φ < 2π
3 . Prove that there
is a point in the space such that all sides of the triangle are visible from it at the angle of φ.

### [Trang 3 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Second olympiad, year 2006
Correspondence round
1. (8) Two lines in the plane, intersecting at an angle of 46◦, serve as symmetry axes for
a geometric ﬁgure F. What is the minimal number of symmetry axes of this ﬁgure?
2. (8-9) Points A and B move at equal speeds along equal circles.
Prove that the
perpendicular bisectors to AB concur at a ﬁxed point.
3. (8-9) There is a map with segments of straight linear roads linking three villages.
The villages themselves are beyond the boundaries of the map. Furthermore the ﬁre
station equidistant from the three villages is located inside the boundaries of the
map but not indicated on the map. Can its location be determined using compass
and ruler if the constructions are to be made within the map only?
4. a) (8) Two squares ABCD and DEFG are given, point E belongs to segment CD,
while points F, G lie outside the square ABCD. Find the angle between the lines
AE and BF.
b) (9-11) Two regular pentagons OKLMN and OPRST are given, where the point P
belongs to segment ON, while the points R, S, T lie outside the pentagon OKLMN.
Find the angle between the lines KP and MS.
5. a) (8) Fold a square 10 × 10 from a rectangular stripe 1 × 118.
b) (9-11) Fold a square 10 × 10 from a rectangular stripe 1 × (100 + 9
√
3) (approxi-
mately 1x115.58).
In each case the stripe can be folded but cannot be ripped into parts.
6. a) (8-9) Given a segment AB with point C inside it. The segment is a chord of the
circle with radius R. Inscribe a circle into the formed circle segment such that this
circle contains point C and is tangent to the initial circle.
b) (9-10) Given a segment AB with point C inside it, which is the tangency point of
this segment with the circle of radius r. Draw a circle through points A and B such
that it is tangent to the initial circle.
7. (8-10) Given are a point E inside the square ABCD and a point F outside it, so
that triangles ABE and BCF are equal. Find the angles of the triangle ABE if it is
known that the segment EF is equal to the side of the square, while the angle BFD
is right.
8. (8-9) The segment AB splits the square into two equal parts. A circle can be inscribed
into each of them. The radii of the circles equal r1 and r2 where r1 > r2. Find the
length of AB.
9. (8-10) Let the line L(α) link the points of the unit circle, corresponding to the angles
α and π −2α. Prove that if α + β + γ = 2π, then the lines L(α), L(β) and L(γ) are
concurrent.
10. (8-11) For what n a regular n-gon can be split by non-intersecting diagonals into
isosceles (and, possibly, equilateral) triangles?

### [Trang 4 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
11. (9-10) Let point O be the center for the circumcircle of the triangle ABC; let A′, B′,
C′ be the points symmetrical to A, B, C about respective opposite sides; let A1, B1,
C1 be the points of intersection between the lines OA′ and BC, OB′ and AC, OC′
and AB. Prove that the lines AA1, BB1, CC1 intersect at the same point.
12. (9-10) In the triangle ABC the bisector of the angle A equals the half-sum of its
median and altitude dropped from the vertex A. Prove that if̸
A is obtuse then
AB = AC.
13. (9-10) Consider two lines a and b, as well as two points A and B. The point X slides
along a, whereas the point Y slides along b, so that AX ∥BY . Find the locus of
intersections between AY and XB.
14. (9-11) Consider a circle and a ﬁxed point P not belonging to it. Find the locus for
orthocenters of triangles ABP, where AB is the circle diameter.
15. (9-11) For a triangle ABC, consider the circumcircle and the incircle, the latter of
which touches its sides BC, CA, AB at points A1, B1, C1 respectively. The line
B1C1 crosses the line BC at the point P, whereas the point M is the midpoint of
the segment PA1. Prove that the segments of the tangents from the point M to the
incircle and to the circumcircle are equal.
16. (9-11) Sides of the triangle ABC are bases for regular triangles drawn outside it.
Their outlying vertices form a regular triangle. Is that true that the initial triangle
is regular?
17. (9-11) In two circles intersecting at points A and B, two parallel chords A1B1 and
A2B2 are drawn. The lines AA1 and BB2 meet at the point X, while the lines AA2
and BB1 meet at the point Y . Prove that XY ∥A1B1.
18. (9-11) Two perpendicular lines are drawn through the orthocenter H of the triangle
ABC. One of them intersects BC at point X, another one intersects AC in point
Y . The lines AZ, BZ are parallel to the lines HX and HY respectively. Prove that
the points X, Y , Z are collinear.
19. (10-11) Through the midpoints of the sides of triangle T, the lines perpendicular
to the bisectors of the opposite angles are drawn. These lines form the triangle T1.
Prove that its circumcenter is the midpoint of the segment linking the incenter and
the orthocenter of T.
20. (10-11) In the plane, consider four points A, B, C, D. The points A1, B1, C1, D1 are
the orthocenters of triangles BCD, CDA, DAB, ABC respectively. The points A2,
B2, C2, D2 are the orthocenters of triangles B1C1D1, C1D1A1, D1A1B1, A1B1C1, and
so on. Prove that all the circles containing the midpoints of sides of these triangles,
intersect in the same point.
21. (10-11) Consider points C′, A′, B′ on the sides AB, BC, CA of the triangle ABC.
Prove that the following inequality holds for areas of respective triangles:
SABCS2
A′B′C′ ≥4SAB′C′SBC′A′SCA′B′;
moreover, the equality holds only if the lines AA′, BB′, CC′ concur.

### [Trang 5 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
22. (10-11) Consider a circle and points A and B on it, as well as a point P in the plane.
Let X be an arbitrary point of the circle, Y be the commom point of lines AX and
BP. Find the locus of circumcenters of the triangles PXY .
23. Consider a convex quadrilateral ABCD, and let G be its center of mass as of a
uniform plate (i.e., the point of intersection of two lines each of which links centroids
of triangles sharing the same diagonal).
a) (9-10) Suppose a circle can be circumscribed about ABCD, a point O being its
center. Let us deﬁne point H similarly to point G by taking orthocenters instead of
centroids. Prove that the points H, G, O are collinear, and HG : GO = 2 : 1.
b) (10-11) Suppose a circle with center at point I is inscribed to ABCD. Let Nagel
point N of a circumscribed quadrilateral denote the intersection of two lines, each
of which links the points on the opposite sides of the quadrilateral, symmetrical to
the tangent points of the incircle about midpoints of the sides. (These lines split
perimeter of the quadrilateral in two equal parts). Prove that N, G, I are collinear,
whereby NG : GI = 2 : 1.
24. a) (9-10) Consider the point P ﬁxed within the circle and two perpendicular rays
passing through it and crossing the circle at points A and B. Find the locus of
projections of P on the lines AB.
b) (10-11) Consider the point P ﬁxed within the sphere and three pairwise-perpendicular
rays passing through it and crossing the sphere at points A, B, C. Find the locus of
projections of P on the plane ABC.
25. (11) In tetrahedron ABCD the dihedral angles at edges BC, CD and DA are equal
to α, whereas the dihedral angles at the remaining edges are equal to β. Find the
ratio of AB/CD.
26. (11) Four cones with a common vertex and equal length of the generatrix are given.
Radii of their bases are possibly not equal. Each of the cones is tangent with two
others. Prove that the four tangent points of the circle bases of the cones are con-
cyclic.

### [Trang 6 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
I
I
I
GEOMETRICAL
OL
YMPIAD
IN
HONOUR
OF
I.F.SHAR
YGIN
THE
CORRESPONDENCE
R
OUND
1.
(8)
A
triangle
is
 ut
in
to
sev
eral
(not
less
than
t
w
o)
triangles.
One
of
them
is
isos eles
(not
equilateral),
and
all
others
are
equilateral.
Determine
the
angles
of
the
original
triangle.
2.
(8)
Ea 
h
diagonal
of
a
quadrangle
divides
it
in
to
t
w
o
isos eles
triangles.
Is
it
true
that
the
quadrangle
is
a
diamond?
3.
(8-9)
Segmen
ts
 onne ting
an
inner
p
oin
t
of
a
 on
v
ex
non-equilateral
n-gon
to
its
v
erti es
divide
the
n-gon
in
to
n
equal
triangles.
What
is
the
least
p
ossible
n?
4.
(8)
Do
es
a
parallelogram
exist
su 
h
that
all
pairwise
meets
of
bisse tors
of
its
angles
are
situated
outside
it?
5.
A
non- on
v
ex
n-gon
is
 ut
in
to
three
parts
b
y
a
straigh
t
line,
and
t
w
o
parts
are
put
together
so
that
the
resulting
p
olygon
is
equal
to
the
third
part.
Can
n
b
e
equal
to:
a)
(8)
v
e?
b)
(8-10)
four?
6.
a)
(8-9)
What
 an
b
e
the
n
um
b
er
of
symmetry
axes
of
a

he 
k
ed
p
olygon,
that
is,
of
a
p
olygon
whose
sides
lie
on
lines
of
a
list
of

he 
k
ed
pap
er?
(Indi ate
all
p
ossible
v
alues.)
b)
(10-11)
What
 an
b
e
the
n
um
b
er
of
symmetry
axes
of
a

he 
k
ed
p
olyhedron,
that
is,
of
a
p
olyhedron
 onsisting
of
equal
 ub
es
whi 
h
b
order
one
to
another
b
y
plane
fa ets?
7.
(8-9)
A
 on
v
ex
p
olygon
is
 ir ums rib
ed
around
a
 ir le.
P
oin
ts
of
 on
ta t
of
its
sides
with
the
 ir le
form
a
p
olygon
with
the
same
set
of
angles
(the
order
of
angles
ma
y
dier).
Is
it
true
that
the
p
olygon
is
regular?
8.
(8-9)
Three
 ir les
pass
through
a
p
oin
t
P
,
and
the
se ond
p
oin
ts
of
their
in
terse tion
A,
B
,
C
lie
on
a
straigh
t
line.
Let
A
,
B
,
C
b
e
the
se ond
meets
of
lines
AP
,
B
P
,
C
P
with
the
 orresp
onding
 ir les.
Let
C
b
e
the
meet
of
lines
AB
and
B
A
.
Let
A
,
B
b
e
dened
similarly
.
Pro
v
e
that
the
triangles
A
B
C
and
A
B
C
are
equal.
9.
(8-9)
Supp
ose
t
w
o
 on
v
ex
quadrangles
are
su 
h
that
the
sides
of
ea 
h
of
them
lie
on
the
middle
p
erp
endi ulars
to
the
sides
of
the
other
one.
Determine
their
angles.
10.
(8-9)
Find
the
lo
 us
of
 en
ters
of
regular
triangles
su 
h
that
three
giv
en
p
oin
ts
A,
B
,
C
lie
resp
e tiv
ely
on
three
lines
 on
taining
sides
of
the
triangle.
11.
(8-10)
A
b
o
y
and
his
father
are
standing
on
a
seashore.
If
the
b
o
y
stands
on
his
tipto
es,
his
ey
es
are
at
a
heigh
t
of
m
ab
o
v
e
sea-lev
el,
and
if
he
seats
on
father's
shoulders,
they
are
at
a
heigh
t
of
m.
What
is
the
ratio
of
distan es
visible
for
him
in
t
w
o
 ases?
(Find
the
answ
er
to
0.1,
assuming
that
the
radius
of
Earth
equals
km.)

### [Trang 7 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
12.
(9-10)
A
re tangle
AB
C
D
and
a
p
oin
t
P
are
giv
en.
Lines
passing
through
A
and
B
and
p
erp
endi ular
to
P
C
and
P
D
resp
e tiv
ely
,
meet
at
a
p
oin
t
Q.
Pro
v
e
that
P
Q
?
AB
.
13.
(9-10)
On
the
side
AB
of
a
triangle
AB
C
,
t
w
o
p
oin
ts
X
,
Y
are

hosen
so
that
AX
=
B
Y
.
Lines
C
X
and
C
Y
meet
the
 ir um ir le
of
the
triangle,
for
the
se ond
time,
at
p
oin
ts
U
and
V
.
Pro
v
e
that
all
lines
U
V
(for
all
X
;
Y
,
giv
en
A;
B
;
C
)
ha
v
e
a
 ommon
p
oin
t.
14.
(9-11)
In
a
trap
ezium
with
bases
AD
and
B
C
,
let
P
and
Q
b
e
the
middles
of
diagonals
AC
and
B
D
resp
e tiv
ely
.
Pro
v
e
that
if
D
AQ
=
C
AB
then
P
B
A
=
D
B
C
.
15.
(9-11)
In
a
triangle
AB
C
,
let
AA
,
B
B
and
C
C
b
e
the
bisse tors.
Supp
ose
A
B
\
C
C
=
P
and
A
C
\
B
B
=
Q.
Pro
v
e
that
P
AC
=
QAB
.
16.
(9-11)
On
t
w
o
sides
of
an
angle,
p
oin
ts
A,
B
are

hosen.
The
middle
M
of
the
segmen
t
AB
b
elongs
to
t
w
o
lines
su 
h
that
one
of
them
meets
the
sides
of
the
angle
at
p
oin
ts
A
,
B
,
and
the
other
at
p
oin
ts
A
,
B
.
The
lines
A
B
and
A
B
meet
AB
at
p
oin
ts
P
and
Q.
Pro
v
e
that
M
is
the
middle
of
P
Q.
17.
(9-11)
What
triangles
 an
b
e
 ut
in
to
three
triangles
ha
ving
equal
radii
of
 ir um-
 ir les?
18.
(9-11)
Determine
the
lo
 us
of
v
erti es
of
triangles
whi 
h
ha
v
e
pres rib
ed
ortho
 en
ter
and
 en
ter
of
 ir um ir le.
19.
(10-11)
In
to
an
angle
A
of
size

,
a
 ir le
is
ins rib
ed
tangen
t
to
its
sides
at
p
oin
ts
B
and
C
.
A
line
tangen
t
to
this
 ir le
at
a
p
oin
t
M
meets
the
segmen
ts
AB
and
AC
at
p
oin
ts
ò
and
Q
resp
e tiv
ely
.
What
is
the
minim
um

su 
h
that
the
inequalit
y
S
P
AQ
<
S
B
M
C
is
p
ossible?
20.
(11)
The
base
of
a
p
yramid
is
a
regular
triangle
ha
ving
side
of
size
1.
Tw
o
of
three
angles
at
the
v
ertex
of
the
p
yramid
are
righ
t.
Find
the
maxim
um
v
alue
of
the
v
olume
of
the
p
yramid.
21.
(11)
There
are
t
w
o
pip
es
on
the
plane
(the
pip
es
are
 ir ular
 ylinders
of
equal
size,
m
around).
Tw
o
of
them
are
parallel
and,
b
eing
tangen
t
one
to
another
in
the
 ommon
generatrix,
form
a
tunnel
o
v
er
the
plane.
The
third
pip
e
is
p
erp
endi ular
to
t
w
o
others
and
 uts
out
a

ham
b
er
in
the
tunnel.
Determine
the
area
of
the
surfa e
of
this

ham
b
er.

### [Trang 8 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
 
	 
	   !
!
"
#$ &%'#%)(*+
, 
+-.
//(*0
+1!2
"+
3547698:,;<=4?>A@B4DC78EBFBGH>AG98EBIJ8KL>M;I=NOIPC78EBIQ>AGH>ARS>AG9EBTU>A@B4VC78<=<=47I=WB8EBFB47EBC74X<=8RBEBF18KL>A@B4DY)Z[T478\]4^>Q_
<=G9C`;6a86Hb\]WBGc;FdG9E1@B8EB8RB<*8KeYMf
g5fih@&;<QbTG9Eaf
jk;<Q>AG9C7G9W&;l>AG98EmG9Em>A@B4P86Hb\]WBGc;FmG9IkWB8I=I=G9nB694*K'8<oWBRBWBG969Ik8Kqpsrutt*K'8<=\]IPvw>A@B47I=4?;<=4*K'8RB<k4769FB47<oK'8<=\]I
G9ExyRBI=I=Gc;E1I=C7@B886wz{f&Y|E1>A@B4D69G9IQ>*8KL>M;I=NOIPWB<=47I=47ES>A47F}nB47698:D~&4`;C7@1>M;I=NG9I*G9EBFBG9C`;l>A47F1nSbd>A@B4DEBRB\]nB47<=I
8KqK'8<=\]I5K'8<:y@BG9C7@GH>JG9IJG9ES>A47EBFB47FafBP8:y4^47<*>A@B4?W&;<Q>AG9C7G9W&;ES>AI5\;lb]I=86H4>A@B4?>M;I=NOIJK'8<54769FB47<5K'8<=\]I
;I*:y47696f
V8RB<:y8<=NG9E.;}I=C7@B8865C78WSb_|nB88NC78ES>M;G9EBG9EBT>A@B4dI=869RS>AG98EBIDK'8<>A@B4]>M;I=NOIm\]RBIQ>UnB4dI=47ES>`~;l>
>A@B4P6c;l>A47IQ>`~OWB<=G96t~pD>A8D>A@B4PK'869698:yG9EBTD;FBFB<=47I=I7SxyRBI=I=Gc;S~tts~8I=C78:D~S35869I=@B8bmZ?6c;IQb4^I=Nb
WB47<7fH~qttf?6Hb\]WBGc;FdG9E1@B8EB8RB<y8KeYMf
g5fih@&;<QbTG9Eaf
*@B4d:y8<=N\]RBIQ>UnB4:y<=GH>=>A47E.G9ExyRBI=I=Gc;E.8<XG9E.oEBT69G9I=@af?E0>A@B4dC7847<m8K*>A@B4dC78WSb_|nB88N~L>A@B4
K'869698:yG9EBTG9ESK'8<=\;l>AG98EG9I8nB47FBG947ES>`e;696kE&;\]47Idv'RBEBFB47<=69G9EB4>A@B4dI=RB<=E&;\]4sz{WB8IQ>m;FBFB<=47I=IUG9EBC769RBFBG9EBT
WB8IQ>DG9EBFB4{~aWB@B8EB4mEBRB\]nB47<D;EBFl8<Ve_|\;G96&>A@B4mEBRB\]nB47<V8Kkb8RB<VWB<=47I=47ES>DK'8<=\u>A@B4mEBRB\]nB47<V;EBF
;FBFB<=47I=I58Kb8RB<I=C7@B886K'RB696&E&;\]47Ik8Kb8RB<k>A4`;C7@B47<=I5G9E]\;l>A@BI;EBFl8<k8KqG9EBIQ>A<=RBC^>A8<=Ik8Kb8RB<\;l>A@
C7G9<=C7694f
jo694`;I=4?:y<=GH>A4?FB8:yE4`;C7@>M;I=N]K'<=8\;UEB4^:+W&;T4K'G9<=IQ>J:y<=GH>A4?FB8:yEd>A@B4VC78EBFBGH>AG98Ea~S;EBFd>A@B47E>A@B4
I=869RS>AG98Eafsjo<=47I=47ES>b8RB<LI=869RS>AG98EDG9EFB4^>M;G96~`G9EBC769RBFBG9EBTP;69647I=I=47ES>AGc;6;<=TRB\]47ES>AIe;EBFXC`;69C7RB6c;l>AG98EBI7~7:yGH>A@
4{B;C^>K'G9TRB<=47I7f*@B4*I=869RS>AG98EX8Ku;?C78\]WBRS>M;l>AG98E&;6>M;I=N\]RBIQ>onB4JC78\]WB694^>A47FUnSbm;FBG9IQ>AG9EBC^>A6HbWB<=47I=47ES>A47F
;EBIQ:y47<7fejo694`;I=4nB4;C7C7RB<A;l>A4b8R;<=4G9ES>A47<=47IQ>A47F0G9ET88FRBEBFB47<=IQ>M;EBFBG9EBT;EBF>A<=RB4]47IQ>AG9\;l>AG9EBT8K
b8RB<*:y8<=N
Y)Kb8RB<PI=869RS>AG98EFB47WB47EBFBI?8E}I=8\]4V:y47696_|NOEB8:yE>A@B478<=47\8<P;K;C^>PK'<=8\ ;]IQ>M;EBF&;<=F}>A4{>AnB88N~
b8Rd\;lbI=G9\]WB6Hbm<=4^K'47<>A8XGH>?v'4{SWB6c;G9EBG9EBTD:y@BG9C7@>A@B478<=47\¡8<kK;C^>JG9IRBI=47Fz{fS35RS>JGHKab8RdRBI=4?;DK;C^>JEB8>
C78ES>M;G9EB47F1G9E>A@B4DC7RB<=<=G9C7RB69RB\~b8R@&;l4V>A8WB<=84GH>v'8<J>A8G9EBFBG9C`;l>A4?>A@B4DI=8RB<=C74sz{f
V8RB<P:y8<=N1:yG9696LnB4>A@B8<=8RBT@B6Hb4{B;\]G9EB47Fa~;EBFb8R:yG9696<=47C747GH4X>A@B4m;EBIQ:y47<7~a;l>>A@B4U6c;l>A47IQ>`~uG9E
>A@B4\]G9FBFB694D8K};lb}pSf*@B4:yG9EBEB47<=I8Ke>A@B4XC78<=<=47I=WB8EBFB47EBC74m<=8RBEBF:yG9696qnB4XG9ESGH>A47F1>A8]>A@B4K'G9E&;6
<=8RBEBF1:y@BG9C7@:yG9696nB4@B4769F1G9E1I=RB\]\]47<PpUG9E¢RBnBE&;}v'EB4`;<8I=C78:z{f
tfXvpzX¢847I;<=47TRB6c;<UWB86HbT8E4{SG9IQ>I=RBC7@.>A@&;l>£=RBIQ>m@&;6HKP8KPGH>AIXFBGc;T8E&;69IU;<=4dW&;<A;6969476k>A8GH>AI
I=G9FB47IM¤
fXvpzge8<;DTGH47E]W&;G9<o8KaC7G9<=C76947I7~C78EBIQ>A<=RBC^>>=:y8C78EBC747ES>A<=G9CPC7G9<=C76947IkI=RBC7@]>A@&;l>nB8>A@;<=4*>M;EBT47ES>
>A8m>A@B4DTGH47E>=:y8BfB¥@&;l>yG9I*>A@B4DEBRB\]nB47<*8KeI=869RS>AG98EBI7~BFB47WB47EBFBG9EBT]8E1698C`;l>AG98E8KL>A@B4DC7G9<=C76947IM¤
¦
fXvpzV§>A<=Gc;EBT694mC`;EnB4dFBG9I=I=47C^>A47F.G9ES>A81>A@B<=474d47¨OR&;6k>A<=Gc;EBT6947I7fLjo<=84]>A@&;l>XI=8\]4GH>AIX;EBT694]G9I
47¨OR&;6a>A8]©ª«7f
¬
fXvpsrSz*@B4DnBG9I=47C^>A8<=Iy8K>=:y8;EBT6947IJG9E;E1G9EBI=C7<=G9nB47F1¨OR&;FB<A;EBT694D;<=4VW&;<A;6969476fjo<=84V>A@&;l>*>A@B4
I=RB\$8KPI=¨OR&;<=47I]8KI=8\]4>=:y8I=G9FB47ImG9E>A@B41¨OR&;FB<A;EBT69447¨OR&;69IU>A@B41I=RB\$8KPI=¨OR&;<=47I]8Ky>=:y8
<=47\;G9EBG9EBTUI=G9FB47I7f
­
fXvpsrSzxy47C78EBIQ>A<=RBC^>y>A@B4VI=¨OR&;<=4D®?¯U°±}~STGH47E1GH>AI547<Q>A4{1®²;EBF1FBG9IQ>M;EBC747I*8K47<Q>AG9C747IP¯³;EBF
±´K'<=8\´;UK'GS47FWB8G9ES>yµ¶G9E>A@B4DWB6c;EB4f
·
fXvp¸_¹zY|E1>A@B4DWB6c;EB4~BTGH47E1>=:y8C78EBC747ES>A<=G9CC7G9<=C76947IJ:yGH>A@>A@B4DC747ES>A47<P®Xf&ºq4^>¯¡nB4;E};<=nBGH>A<A;<Qb
WB8G9ES>58EI=8\]48Ka>A@B47I=4?C7G9<=C76947I7~S;EBF°!8E]>A@B4?8>A@B47<58EB4fSge8<4^47<Qb]>A<=Gc;EBT694y®?¯U°~C78EBI=G9FB47<
>=:y847¨OR&;6DC7G9<=C76947I1\]RS>AR&;696Hb>M;EBT47ES>};l>1>A@B4WB8G9ES>»~yI=RBC7@¼>A@&;l>8EB48KX>A@B47I=4C7G9<=C76947I1G9I
>M;EBT47ES>P>A8]>A@B469G9EB4D®?¯;l>WB8G9ES>?¯;EBF>A@B4X8>A@B47<P8EB4G9Iy>M;EBT47ES>P>A8]>A@B4X69G9EB4V®?°§;l>PWB8G9ES>
°f&¢4^>A47<=\]G9EB4V>A@B4D698C7RBI*8KeWB8G9ES>AIy»f
t

### [Trang 9 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
½
fXvpsrSzk¾VGH47Ed;XC7G9<=C7694P;EBF;WB8G9ES>5µ!8EdGH>`fEB8>A@B47<5C7G9<=C7694y:yGH>A@C747ES>A47<Jµ!\]474^>AI>A@B4PK'G9<=IQ>8EB4
;l>WB8G9ES>AI?¿§;EBFÀfu*@B4UWB8G9ES>?°¡69G947IP8E}>A@B4XK'G9<=IQ>C7G9<=C7694~u;EBF>A@B4X69G9EB47I°¿~°À¡\]474^>>A@B4
I=47C78EBFC7G9<=C7694?K'8<J>A@B4DI=47C78EBF>AG9\]4V;l>yWB8G9ES>AI*®[;EBF}¯f&jo<=84D>A@&;l>y®?¯ÂÁ+¿Àf
pSfXvpsrutt¸zL;zejo<=84*>A@&;l>K'8<ÃÄÅB~;ESbUC78ES4{Ã_|T8EmC`;EnB4*FBG9I=I=47C^>A47F]G9ES>A8VÃd8nS>ARBI=4*>A<=Gc;EBT6947I7f
nz*jo<=84D>A@&;l>yK'8<y;ESb1Ãe~B>A@B47<=44{SG9IQ>AI;C78ES4{}Ã_|T8E:y@BG9C7@}C`;EBEB8>PnB4FBG9I=I=47C^>A47F}G9ES>A86947I=I
>A@&;E1Ã8nS>ARBI=4V>A<=Gc;EBT6947I7f
CszyY|E;FBG9I=I=47C^>AG98E8Kk;<=47C^>M;EBT694XG9ES>A88nS>ARBI=4X>A<=Gc;EBT6947I7~&:y@&;l>VG9Iy>A@B4U694`;IQ>?WB8I=I=G9nB694EBRB\]nB47<
8KL>A<=Gc;EBT6947IM¤
SfXvsrutsz*@B4D69G9EB47I*IQb\]\]4^>A<=G9C`;6u>A8FBGc;T8E&;6a¯U± 8K;m<=47C^>M;EBT694V®?¯U°± <=476c;l>AGH4>A8nBG9I=47C^>A8<=I
8KU;EBT6947I1¯Æ;EBF+±ÇW&;I=I>A@B<=8RBT@>A@B4\]G9FBWB8G9ES>d8KXFBGc;T8E&;6®?°fyjo<=84>A@&;l>>A@B469G9EB47I
IQb\]\]4^>A<=G9C`;6>A8FBGc;T8E&;65®?°È<=476c;l>AGH4>A8nBG9I=47C^>A8<=I8K;EBT6947Im®;EBF°ÈW&;I=Im>A@B<=8RBT@.>A@B4
\]G9FBWB8G9ES>J8KeFBGc;T8E&;6a¯U±}f
tsSfXvsrutszkÉ?R&;FB<A;EBT694P®?¯U°±§G9I5C7G9<=C7RB\]I=C7<=G9nB47Fd;<=8RBEBF;C7G9<=C7694y:yGH>A@C747ES>A47<JÊfjo<=84>A@&;l>>A@B4
WB<=8{£=47C^>AG98EBI*8KeWB8G9ES>AIy¯§;EBF± >A8m>A@B4D69G9EB47IJÊO®[;EBFÊ°Â69G94?8E;I=G9EBT694?C7G9<=C7694f
ttfXvsrutszD¾VGH47E0K'8RB<WB8G9ES>AI®X~e¯~e°~e±}fLESb>=:y8C7G9<=C76947IXI=RBC7@0>A@&;l>U8EB48KJ>A@B47\ËC78ES>M;G9EBI
®¶;EBF¯~;EBF>A@B4U8>A@B47<8EB4UC78ES>M;G9EBI?°§;EBF±}~u\]474^>`fjo<=84X>A@&;l>?C78\]\]8E}C7@B8<=FBIV8K;696
>A@B47I=4DW&;G9<=I*8KeC7G9<=C76947IyW&;I=I*>A@B<=8RBT@;C78\]\]8EWB8G9ES>`f
t¸fXvsrutszy¾VGH47E;>A<=Gc;EBT694D®?¯U°fjo8G9ES>P®DÌyG9IPC7@B8I=47E8E>A@B4X<A;lb}¯X®ÂI=8]>A@&;l>?I=47T\]47ES>AI?¯X®DÌ
;EBF1¯U°¶;<=4V47¨OR&;6f&jo8G9ES>*®ÍyG9IJC7@B8I=47E8E>A@B4V<A;lb°D®²I=8m>A@&;l>*I=47T\]47ES>AIP°D®ÍP;EBF¯U°Â;<=4
47¨OR&;6fjo8G9ES>AI5¯DÌ^~S¯Í*;EBFd°PÌ^~°JÍ*;<=4PC7@B8I=47EI=G9\]G96c;<=6Hbufjo<=84>A@&;l>569G9EB47I®DÌ¹®Ís~¯DÌ=¯Í`~S°PÌQ°JÍ
;<=4VW&;<A;6969476f
t
¦
fXvsrutsz?¾VGH47E>A<=Gc;EBT694X®?¯U°fL?EB48KJGH>AIV4{SC7G9<=C76947IDG9I?>M;EBT47ES>D>A8>A@B4I=G9FB4]¯U° ;l>DWB8G9ES>D®DÌ
;EBFd>A8U>A@B4V4{>A47EBI=G98EBIy8K>=:y88>A@B47<JI=G9FB47I7fBEB8>A@B47<*4{SC7G9<=C7694VG9I5>M;EBT47ES>J>A8mI=G9FB4V®?°Â;l>*WB8G9ES>
¯DÌ{fh47T\]47ES>AIy®®DÌ*;EBF¯U¯DÌJ\]474^>P;l>*WB8G9ES>yÎfjo8G9ES>P¿[G9I*C7@B8I=47E8E>A@B4V<A;lb®®DÌ5I=8>A@&;l>
®?¿²Á¼Î®DÌ7f&jo<=84V>A@&;l>¿Â69G947IJ8E1>A@B4DG9EBC7G9<=C7694f
t
¬
fXvsrutszk*@B4D69G9EB4?C78EBEB47C^>AG9EBTU>A@B4DG9EBC747ES>A47<y;EBF>A@B4V8<Q>A@B8C747ES>A47<*8K;UEB8E_|G9I=8I=C7476947IJ>A<=Gc;EBT694G9I
W&;<A;6969476>A8>A@B4DnBG9I=47C^>A8<*8Ke8EB4D8KeGH>AIy;EBT6947I7f&¢4^>A47<=\]G9EB4V>A@BG9Iy;EBT694f
t
­
fXvsrutt¸z¾VGH47E>=:y81C7G9<=C76947IV;EBFWB8G9ES>D¿§EB8>V6HbG9EBTd8E>A@B47\fa¢<A;l:¶;69G9EB4>A@B<=8RBT@¿¡:y@BG9C7@
C7RS>AIyC7@B8<=FBIy8K47¨OR&;6q6947EBT>A@K'<=8\§>A@B47I=4C7G9<=C76947I7f
t
·
fXvsrutt¸z¾VGH47Ed>=:y8UC7G9<=C76947I7fS*@B47G9<5C78\]\]8Ed4{>A47<=E&;6u>M;EBT47ES>*G9I>M;EBT47ES>J>A8X>A@B47\´;l>JWB8G9ES>AI5®
;EBFd¯fSjo8G9ES>AIÏ.~Ð[8E>A@B47I=4C7G9<=C76947IJ;<=4PI=RBC7@d>A@&;l>JI=8\]4PC7G9<=C7694PG9Ik>M;EBT47ES>5>A8>A@B4TGH47E]>=:y8
C7G9<=C76947I;l>>A@B47I=4UWB8G9ES>AI7~;EBFG9E}I=G9\]G96c;<J:P;lb.v'4{>A47<=E&;6e8<PG9ES>A47<=E&;6wz{fu¢4^>A47<=\]G9EB4>A@B4X698C7RBI8K
G9ES>A47<=I=47C^>AG98EBI*8Ke69G9EB47I*®PÏÑ;EBF}¯UÐ]f
t
½
fXvsrutt¸z¾VGH47E>A<=Gc;EBT694y®?¯U°Â;EBF1;X<=RB6947<:yGH>A@>=:y8U\;<=NO47FdG9ES>A47<QS;69I547¨OR&;6u>A8U®?°Â;EBF¯U°f
3bd>A@BG9I*<=RB6947<*8EB6Hbu~SK'G9EBF>A@B4DG9EBC747ES>A47<y8KL>A@B4V>A<=Gc;EBT694PK'8<=\]47F1nSb\]G9FB69G9EB47I58KL>A<=Gc;EBT694?®?¯U°f
tspSfXvsrutt¸z5jo<=84V>A@&;l>y>A@B4V>A<=Gc;EBT694@&;lG9EBTI=G9FB47IPÒ&~Ós~ÔV;EBF;<=4`;Õ
IA;l>AG9IQK'G947IJ>A@B4DG9EB47¨OR&;69GH>=b
Ò
ÍÖ
Ó
ÍÖ
Ô
Í×¶Ø
ÙÚMÛ
Ò
×
Ó
Û
Ö
Û
Ó
×
Ô
Û
Ö
Û
Ô
×
Ò
Û
Ü
ÍPÝ
ÅÞ
ßÕeà


### [Trang 10 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
tsSfXv¹ts¸_Mtt¸zy¾VGH47E}W&;<A;696947698T<A;\§®?¯U°±ÈI=RBC7@>A@&;l>®?¯¡Á[Ò&~®?±áÁ!Ósfu*@B4K'G9<=IQ>C7G9<=C7694@&;IGH>AI
C747ES>A47<V;l>47<Q>A4{®³;EBFW&;I=I=47I?>A@B<=8RBT@±}~;EBF}>A@B4UI=47C78EBFC7G9<=C7694@&;IGH>AIC747ES>A47<V;l>V°§;EBF
W&;I=I=47IJ>A@B<=8RBT@1±}f,C7G9<=C7694y:yGH>A@C747ES>A47<*¯¶\]474^>AI5>A@B4K'G9<=IQ>JC7G9<=C7694?;l>JWB8G9ES>AIyâ.Ì{~BÎmÌ^~S;EBFd>A@B4
I=47C78EBFC7G9<=C7694D;l>yWB8G9ES>AIPâÍs~ÎÍ`f¢4^>A47<=\]G9EB4?>A@B4D<A;l>AG98]â.Ì=ÎmÌAã`âÍMÎÍ`f
SfXv¹tssrutt¸z;zmh8\]4dWB86HbT8E.@&;Im>A@B4dK'869698:yG9EBT}WB<=8WB47<Q>=buoGHKP;69G9EB4dW&;I=I=47Im>A@B<=8RBT@;ESb0>=:y8
WB8G9ES>AIJ:y@BG9C7@nBG9I=47C^>PGH>AIyWB47<=G9\]4^>A47<J>A@B47E1>A@BG9Iy69G9EB4?nBG9I=47C^>AIy>A@B4;<=4`;8KL>A@B4WB86HbT8EafBY|IyGH>*>A<=RB4
>A@&;l>*>A@B4DWB86HbT8E1G9I*C747ES>A<A;6qIQb\]\]4^>A<=G9C`;6w¤
nz5Y|IyGH>*>A<=RB4V>A@&;l>P;ESbdK'G9TRB<=4?:yGH>A@>A@B4DWB<=8WB47<Q>=bdK'<=8\W&;<Q>;z5G9I*C747ES>A<A;6qIQb\]\]4^>A<=G9C`;6w¤
tfXv¹tssrutt¸zY|Ed;>A<=Gc;EBT694~8EB4@&;I5FB<A;l:yEd\]G9FBFB694*WB47<=WB47EBFBG9C7RB6c;<=I>A8XGH>AII=G9FB47IJ;EBF@&;I5\]4`;I=RB<=47F
>A@B47G9<*I=47T\]47ES>AIy6HbG9EBTmG9EBI=G9FB4?>A@B4V>A<=Gc;EBT694f
;z5696>A@B<=474DI=47T\]47ES>AIP;<=4D47¨OR&;6fBY|IyGH>*>A<=RB4V>A@&;l>*>A@B4V>A<=Gc;EBT694?G9I*47¨ORBG96c;l>A47<A;6w¤
nz5J:y8]I=47T\]47ES>AI;<=4V47¨OR&;6f&Y|IyGH>J>A<=RB4V>A@&;l>y>A@B4V>A<=Gc;EBT694G9I*G9I=8I=C7476947IM¤
Csz*äJ;E1>A@B4DI=47T\]47ES>AIP@&;l4D6947EBT>A@
¬
~
¬
;EBF
¦
¤
fXv¹tssrutt¸z5;zJ69647<Q>AG9C747IP8Ko;WSb<A;\]G9F169G94?8E1>A@B4VK;C74^>AIP8Ko;mC7RBnB4XnBRS>PEB8>P8EGH>AI*47FBT47I7~u;EBF
4`;C7@K;C74^>UC78ES>M;G9EBIm;l>U694`;IQ>U8EB447<Q>A4{fe¥@&;l>UG9IX>A@B4\;¸SG9\]RB\åWB8I=I=G9nB694EBRB\]nB47<U8K*>A@B4
47<Q>AG9C747Iy8KL>A@B4DWSb<A;\]G9F¤
nz696S47<Q>AG9C747I58Ka;DWSb<A;\]G9F69G94*G9E>A@B4*K;C74^>5WB6c;EB47Ik8Kq;VC7RBnB4nBRS>EB8>8E>A@B4P69G9EB47IoG9EBC769RBFBG9EBT
GH>AI47FBT47I7~;EBFX4`;C7@XK;C74^>eWB6c;EB4C78ES>M;G9EBIe;l>e694`;IQ>e8EB4k47<Q>A4{fl¥@&;l>eG9I>A@B4\;¸SG9\]RB\,WB8I=I=G9nB694
EBRB\]nB47<*8KL>A@B4V47<Q>AG9C747IP8KL>A@B4DWSb<A;\]G9F¤

¦
fXv¹tssrutt¸zY|E>A@B4I=W&;C74~*TGH47E>=:y8
G9ES>A47<=I=47C^>AG9EBT.I=WB@B47<=47I8KFBGHKwK'47<=47ES><A;FBG9G?;EBF¼;.WB8G9ES>d®
nB47698EBTG9EBTm>A8]nB8>A@I=WB@B47<=47I7fajo<=84D>A@&;l>y>A@B47<=4XG9IP;WB8G9ES>¯¡G9E1>A@B4I=W&;C74D:yGH>A@>A@B4DK'869698:yG9EBT
WB<=8WB47<Q>=buGHK;E};<=nBGH>A<A;<QbC7G9<=C7694VW&;I=I=47IP>A@B<=8RBT@}WB8G9ES>AIy®[;EBF¯³>A@B47E>A@B4I=47C78EBFWB8G9ES>AIy8K
GH>AI*\]474^>*:yGH>A@>A@B4DTGH47EI=WB@B47<=47I;<=4V47¨ORBG9FBG9IQ>M;ES>yK'<=8\´¯f

¬
fXv¹tt¸zºq4^>]æ.nB4>A@B4d694`;IQ>m;6H>AGH>ARBFB48KP;>A4^>A<A;@B47FB<=8Ea~o;EBF
ç>A@B4d694`;IQ>mFBG9IQ>M;EBC74dnB4^>=:y4747E
GH>AI
8WBWB8I=GH>A4V47FBT47I7fuge8<5:y@&;l>yS;69RB47Iy8KLè5>A@B4DG9EB47¨OR&;69GH>=bdç]Ä/è=æG9I*WB8I=I=G9nB694s¤
ge47476K'<=474>A8P;I=N?;ESb?¨ORB47IQ>AG98EBIqGc;y?<=T;EBG9é7G9EBT5C78\]\]GH>=>A474e8KwK'G9C7Gc;6l4{_|\;G96êOësìlíìlîðïlíñeòJíósó^íë`ô9õ{ö
¦

### [Trang 11 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
V GEOMETRICAL OLYMPIAD IN HONOUR OF I.F.SHARYGIN
THE CORRESPONDENCE ROUND
Below are the conditions for the correspondence round of the V Geometrical Olympiad in
honour of I.F.Sharygin.
Participation in the olympiad is possible for pupils of 8–11 forms (these are four elder forms
in Russian school). In the list of tasks presented below, each task is indicated by the numbers
of forms for which it is intended. However the participants may solve the tasks for elder forms
as well (the solutions of problems for younger forms will not be considered).
Your work containing the solutions for the tasks (in Russian or English) must be sent, at
the latest, April 1, 2009. We recommend to send the work by e-mail to geomolymp@mccme.ru
in pdf, doc or jpg ﬁles. To avoid the loss of your work, please maintain the following rules.
1. Each work must be sent by a separate message.
2. If your work is contained in several ﬁles send it as an archive.
3. In the subject of the message, write “The work for Sharygin olympiad”, and present the
following information in the text:
- last name, ﬁrst name;
- post address, phone number, E-mail;
- the current number of your form;
- the number and the address of your school;
- full names of your teachers in maths and/or of instructors of your math circle.
If you can’t send your work by e-mail, please send it through the post to the following
address: Russia, 119002, Moscow, Bolshoy Vlasyevsky per., 11. Olympiad in honour of I.F.Sharygin.
In the title page present the information indicated in the item 3 above.
Please write down each task from a new page: ﬁrst write down the condition, and next,
the solution. Present your solution in detail, including all essential arguments and calculations,
with exact ﬁgures. The solution of a computational task must be completed by a distinctly
presented answer. Please be accurate: you are interested in good understanding and correct
estimating of your work!
If your solution depends on some well-known theorem or a fact from a standard textbook,
you may simply refer to it (to explain which theorem or fact is used). But if you use a fact not
contained in the curriculum, you have to prove it (or to indicate the source).
Your work will be thoroughly examined, and you will receive the answer, at the latest, in
the middle of May 2009. The winners of the correspondence round will be invited to the ﬁnal
round which will be held in summer 2009 in Dubna (near Moscow).
1. (8) Points B1 and B2 lie on ray AM, and points C1 and C2 lie on ray AK. The circle with
center O is inscribed into triangles AB1C1 and AB2C2. Prove that the angles B1OB2 and
C1OC2 are equal.
2. (8) Given nonisosceles triangle ABC. Consider three segments passing through diﬀerent
vertices of this triangle and bisecting its perimeter. Are the lengths of these segments
certainly diﬀerent?
3. (8) The bisectors of trapezoid’s angles form a quadrilateral with perpendicular diagonals.
Prove that this trapezoid is isosceles.

### [Trang 12 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
4. (8–9) Let P and Q be the common points of two circles. The ray with origin Q reﬂects
from the ﬁrst circle in points A1, A2, . . . according to the rule “the angle of incidence is
equal to the angle of reﬂection”. Another ray with origin Q reﬂects from the second circle
in the points B1, B2, . . . in the same manner. Points A1, B1 and P occurred to be collinear.
Prove that all lines AiBi pass through P.
5. (8–9) Given triangle ABC. Point O is the center of the excircle touching the side BC.
Point O1 is the reﬂection of O in BC. Determine angle A if O1 lies on the circumcircle of
ABC.
6. (8–9) Find the locus of excenters of right triangles with given hypotenuse.
7. (8–9) Given triangle ABC. Points M, N are the projections of B and C to the bisectors
of angles C and B respectively. Prove that line MN intersects sides AC and AB in their
points of contact with the incircle of ABC.
8. (8–10) Some polygon can be divided into two equal parts by three diﬀerent ways. Is it
certainly valid that this polygon has an axis or a center of symmetry?
9. (8–11) Given n points on the plane, which are the vertices of a convex polygon, n > 3.
There exists k regular triangles with the side equal to 1 and the vertices at the given
points.
a) Prove that k < 2
3n.
b) Construct the conﬁguration with k > 0, 666n.
10. (9) Let ABC be an acute triangle, CC1 its bisector, O its circumcenter. The perpendicular
from C to AB meets line OC1 in a point lying on the circumcircle of AOB. Determine
angle C.
11. (9) Given quadrilateral ABCD. The circumcircle of ABC is tangent to side CD, and the
circumcircle of ACD is tangent to side AB. Prove that the length of diagonal AC is less
than the distance between the midpoints of AB and CD.
12. (9–10) Let CL be a bisector of triangle ABC. Points A1 and B1 are the reﬂections of A
and B in CL; points A2 and B2 are the reﬂections of A and B in L. Let O1 and O2 be
the circumcenters of triangles AB1B2 and BA1A2 respectively. Prove that angles O1CA
and O2CB are equal.
13. (9–10) In triangle ABC, one has marked the incenter, the foot of altitude from vertex
C and the center of the excircle tangent to side AB. After this, the triangle was erased.
Restore it.
14. (9–10) Given triangle ABC of area 1. Let BM be the perpendicular from B to the bisecor
of angle C. Determine the area of triangle AMC.
15. (9–10) Given a circle and a point C not lying on this circle. Consider all triangles ABC
such that points A and B lie on the given circle. Prove that the triangle of maximal area
is isosceles.

### [Trang 13 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
16. (9–11) Three lines passing through point O form equal angles by pairs. Points A1, A2 on
the ﬁrst line and B1, B2 on the second line are such that the common point C1 of A1B1
and A2B2 lies on the third line. Let C2 be the common point of A1B2 and A2B1. Prove
that angle C1OC2 is right.
17. (9–11) Given triangle ABC and two points X, Y not lying on its circumcircle. Let A1,
B1, C1 be the projections of X to BC, CA, AB, and A2, B2, C2 be the projections of Y .
Prove that the perpendiculars from A1, B1, C1 to B2C2, C2A2, A2B2, respectively, concur
iﬀline XY passes through the circumcenter of ABC.
18. (9–11) Given three parallel lines on the plane. Find the locus of incenters of triangles with
vertices lying on these lines (a single vertex on each line).
19. (10–11) Given convex n-gon A1 . . . An. Let Pi (i = 1, . . . , n) be such points on its boundary
that AiPi bisects the area of polygon. All points Pi don’t coincide with any vertex and lie
on k sides of n-gon. What is the maximal and the minimal value of k for each given n?
20. (10–11) Suppose H and O are the orthocenter and the circumcenter of acute triangle
ABC; AA1, BB1 and CC1 are the altitudes of the triangle. Point C2 is the reﬂection of
C in A1B1. Prove that H, O, C1 and C2 are concyclic.
21. (10–11) The opposite sidelines of quadrilateral ABCD intersect at points P and Q. Two
lines passing through these points meet the side of ABCD in four points which are the
vertices of a parallelogram. Prove that the center of this parallelogram lies on the line
passing through the midpoints of diagonals of ABCD.
22. (10–11) Construct a quadrilateral which is inscribed and circumscribed, given the radii
of the respective circles and the angle between the diagonals of quadrilateral.
23. (10–11) Is it true that for each n, the regular 2n-gon is a projection of some polyhedron
having not greater than n + 2 faces?
24. (11) A sphere is inscribed into a quadrangular pyramid. The point of contact of the
sphere with the base of the pyramid is projected to the edges of the base. Prove that
these projections are concyclic.

### [Trang 14 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]

	









		



	





	





	

	



	




			


 !""

	






#
	

	


	




	


	
$


		



%&$
	


&

















'
(

	



	


#


)	
	




	
*
"$
+,",$



-


$


.


/$


&

0


	











	













	




 


!

"








#
$



%
$





	
$%
$

	
	

	



%
$

	







	
%
$
	


	






&

	

	
'


(
	







)




	&


$
$


(




	



0
*	
+,,
-
.
/


0

	

!

	









	

&


(

	


	


	




0




	


	
$

	
	

/



$







/&








	&



	

	

/$












(






(
	



3($






	


&
	


%&$






	


	

	
&




	



	

'
(


3
		$


(






	


4
+,",
5

	




&

(


	





+,",

6


4
"
 
6
	
3

$
	


7




$
	


7




$

	
	


7





+
 









	






Æ







9


	


	







/&
	




 
/


$


$







$

$







:




	



























/&
	
	
7








"

### [Trang 15 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
;
 
	




7









	


	








	







	
















/&
	
	
7

















<
 !=
*




	








$





Æ

/






	


	







>


$


	


	








/&
	
	

$

$



?
 !=
/





	















$





Æ

	


	












/&
	
	



		
	


	




@
 !=
	


		
	
&3














	








	
3






/






	


	







&
/&
	







 !",
9


	



&




/






	


	






&>


	
	








:





=
 !",
*






AA

	
&

		


7
*












	







:


&

	

",
 !""
9
	








&
B







	






	


	
	









""
 !""
*
&3




	
&3



	
	

$
	


	

	

$
	
	

	

	


:


&


"+
=
9


	




	



$




	



		
	













9





	




	


	



	








	






/&
	0







>





	

"1
=
9

	&

&3
7



	
	





*




	



$












/&
	










";
=!",
5
	&

&3
7











	
	












&
/&
	










"<
=!""
9


$








	







$












	


	













	






	







&
/&
	
+


------------------------------------------------------------

## NGUỒN: TUYEN-TAP-CAC-BAI-TOAN-HINH-HOC-KHONG-GIAN-CHAU-NGOC-HUNG
- **Phân hệ:** [HÌNH HỌC KHÔNG GIAN 3D]
- **Tên file:** `tuyen-tap-cac-bai-toan-hinh-hoc-khong-gian-chau-ngoc-hung.pdf` (75 trang)

### [Trang 1 - [HÌNH HỌC KHÔNG GIAN 3D]]
CÁC BÀI TOÁN HÌNH KHÔNG GIAN CHO THI ĐẠI HỌC
- Khối chóp
Bài 1.1. Cho hình chóp S.ABCD có đáy ABCD là hình vuông cạnh a, tam giác SAB đều và

SAD = 900. J là trung điểm SD. Tính theo a thểtích khối tứdiện ACDJ và khoảng cách từD
đến mặt phẳng (ACJ).
Giải:
A
B
D
C
I
S
J
+
(
AD ⊥SA
AD ⊥AB
⇒AD ⊥(SAB)
+ Gọi I là trung điểm AB thì AD ⊥SI (1). Mà ∆SAB đều nên SI ⊥AB(2)
Từ(1) và (2) suy ra SI ⊥(ABCD). Do đó d(J,(ACD)) = 1
2d(S,(ABCD)) = 1
2SI = a
p
4
Từđó suy ra VACDJ = 1
3.1
2.a2.a
p
4
= a3p
24 .
∆BCI vuông tại B nên CI2 = CB2 +BI2 = 5a2
∆SIC vuông tại I nên SC2 = SI2 + IC2 = 2a2
Tương tựSD2 = SC2 = 2a2
∆SCD có CJ là đường trung tuyến nên CJ2 = SC2 +CD2
−SD4
= a2
Xét ∆JAC có JA = a
p
; AC = a
p
2;CJ = a nên tính được cosA = 3
Từđó sin
JAC =
p
4 nên dt(JAC) = 1
2. a
p
.
p
4 = a2p
8
Vậy d(D,(JAC)) =
3.a3p
24
a2p
8
= a
p
7
□
Nhận xét: Có thểtính diện tích tam giác JAC bằng cách lấy hình chiếu của J trên mặt đáy (là
trung điểm H của DI). Trong mặt đáy, kẻHK vuông góc với AC (hay HK song song với BD) với
K thuộc AC thì chỉra được JK vuông góc với AC và tính được JK là đường cao tam giác JAC.
Bài 1.2. Cho hình chóp S.ABCD có đáy ABCD là hình thoi ; hai đường chéo AC = 2
p
3a,BD =
2a và cắt nhau tại O; hai mặt phẳng (SAC) và (SBD) cùng vuông góc với mặt phẳng (ABCD).
Biết khoảng cách từđiểm O đến mặt phẳng (SAB) bằng a
p
4 , tính thểtích khối chóp S.ABCD
theo a.
http://boxmath.vn/

### [Trang 2 - [HÌNH HỌC KHÔNG GIAN 3D]]
Giải:
D
A
C
B
O
S
H
K
I
Từgiảthiết AC = 2a
p
3;BD = 2a và AC,BD vuông góc với nhau tại trung điểm O của mỗi
đường chéo. Ta có tam giác ABO vuông tại O và AO = a
p
3;BO = a, do đó 
ABD = 60o hay tam
giác ABD đều. Từgiảthiết hai mặt phẳng (SAC) và (SBD) cùng vuông góc với mặt phẳng
(ABCD) nên giao tuyến của chúng là SO ⊥(ABCD).
Do tam giác ABD đều nên với H là trung điểm của AB,K là trung điểm của HB ta có DH ⊥AB
và DH = a
p
3;OK//DH và OK = 1
2DH = a
p
2
⇒OK ⊥AB ⇒AB ⊥(SOK) Gọi I là hình chiếu của
O lên SK ta có OI ⊥SK; AB ⊥OI ⇒OI ⊥(SAB), hay OI là khoảng cách từO đến mặt phẳng
(SAB). Tam giác SOK vuông tại O,OI là đường cao ⇒
OI2 =
OK2 +
SO2 ⇒SO = a
2 Diện tích
đáy SABCD = 4S∆ABO = 2.OA.OB = 2
p
3a2; đường cao của hình chóp SO = a
2.
Thểtích khối chóp S.ABCD : VS.ABCD = 1
3SABCD.SO =
p
3a3
□
Bài 1.3. Cho hình chóp S.ABCD có đáy ABCD là hình thoi cạnh bằng 3cm , các cạnh SA =
SB = SC = 3cm. Tam giác SBD có diện tích bằng 6cm2 .Tính thểtích của khối chóp S.ABCD.
Giải:
D
A
C
B
O
S
H
Gọi H là hình chiếu của S trên (ABCD) suy ra H nằm trên BD (Vì SA = SB == SC,BD là trung
trực của AC). Do đó SH đường cao của hình chóp cũng là đường cao của tam giác SBD; Gọi O
là giao điểm của AC và BD. Vì SA = SC = DA = DC nên SO = DO suy ra tam giác SBD là tam
giác vuông tại S. Vì dt(SBD) = 6 và SB = 3 nên SD = 4; suy ra BD = 5,SH = 12
5 .
ABCD là hình thoi có AD = 3,DO = 5
2 nên AO =
p
2
suy ra dt(ABCD) = 5
p
2
.
http://boxmath.vn/

### [Trang 3 - [HÌNH HỌC KHÔNG GIAN 3D]]
VS.ABCD = 1
3SH.dt(ABCD) = 2
p
11.
Vậy thểtích khối chóp S.ABCD bằng 2
p
11(cm3).
□
Bài 1.4. Cho hình chóp S.ABC có SA = 3a (với a > 0); SA tạo với đáy (ABC) một góc bằng 600.
Tam giác ABC vuông tại B,
ACB = 300.G là trọng tâm tam giác ABC. Hai mặt phẳng (SGB)
và (SGC) cùng vuông góc với mặt phẳng (ABC). Tính thểtích hình chóp S.ABC theo a.
Giải:
A
C
B
K
G
S
Gọi K là trung điểm BC. Ta có SG ⊥(ABC);
SAG = 600, AG = 3a
2 .
Từđó AK = 9a
4 ;SG = 3a
p
2
.
Trong tam giác ABC đặt AB = x ⇒AC = 2x;BC = x
p
3.
Ta có AK2 = AB2 +BK2 nên x = 9a
p
14
Vậy VS.ABC = 1
3SG.dt(ABC) = 243
112a3.
□
Bài 1.5. Cho hình chóp S.ABCD có đáy ABCD là hình vuông và tam giác SAB là tam giác
cân tại đỉnh S. Góc giữa đường thẳng SA và mặt phẳng đáy bằng 450, góc giữa mặt phẳng
(SAB) và mặt phẳng đáy bằng 600. Tính thểtích khối chóp S.ABCD, biết rằng khoảng cách
giữa hai đường thẳng CD và SA bằng a
p
6.
Giải:
A
B
C
D
M
N
H
S
P
Gọi H là hình chiếu vuông góc của S lên mặt đáy, M là trung điểm AB và do tam giác SAB
cân tại S nên SM vuông góc với AB và kết hợp với SH vuông góc với đáy suy ra AB vuông góc
với mặt phẳng SMN nên theo giảthiết ta được:
á
(SA,(ABCD)) = 
SAH = 450 ⇒SA = SH
p
2.
á
((SAB),(ABCD)) =
á
(SM,MH) = 
SMH = 600 ⇒SM = SH. 2
p
.
http://boxmath.vn/

### [Trang 4 - [HÌNH HỌC KHÔNG GIAN 3D]]
Từđiểm N kẻNP vuông góc với SM thì dễthấy NP là khoảng cách giữa hai đường thẳng SA
và CD suy ra NP = a
p
6. Ta có SH.MN = NP.SM ⇐⇒SH.AB = a
p
6.SH ⇐⇒AB = 2
p
2a
Trong tam giác SAM ta có SA2 = AM2 + SM2 ⇐⇒2.SH2 = 4SH2
+2a2 ⇐⇒SH = a
p
3.
Vậy VS.ABCD = 1
3SH.dt(ABCD) = a
p
3.8a2
= 8
p
3a3
.
□
Bài 1.6. Cho hình chóp S.ABCD có đáy ABCD là hình chữnhật AB = a,BC = 2a. Cạnh bên
SA vuông góc với mặt đáy, SA = a. Gọi H là hình chiếu của A trên SB. Tính thểtích khối
chóp H.ACD theo a và côsin của góc giữa hai mặt phẳng (SBC) và (SCD).
Giải:
A
B
C
D
S
H
E
K
KẻHE//SA(E ∈AB) ⇒HE ⊥(ABCD).
Trong tam giác SAB có AB2 = BH.SB ⇒BH
SB = AB2
SB2 = 1
2 = HE
SA ⇒HE = a
Diện tích ∆ACD là S∆ACD = 1
2 AD.CD = a2 ⇒thểtích H.ACD là VH.ACD = 1
3HE.S∆ACD = a3
SA ⊥(ABCD) ⇒SA ⊥BC mà BC ⊥AB nên BC ⊥(SAB) ⇒BC ⊥HA mà HA ⊥SB nên HA ⊥
(SBC) tương tựgọi K là hình chiếu của A trên SD thì AK ⊥(SCD) do vậy góc giữa hai mặt
phẳng (SBC) và (SCD) là góc giữa AH và AK.
trong tam giác vuông SAB có
AH2 =
AB2 +
SA2 ⇒AH = a
p
2
,SA2 = SH.SB ⇒SH = a
p
2
tương tựAK = 2a
p
,SK = a
p
cos
BSD = SB2 + SD2 −BD2
2.SB.SD
= SH2 + SK2 −HK2
2.SH.SK
⇒HK2 = a2
Trong ∆AHK có cos 
AHK = AH2 + AK2 −HK2
2.AH.AK
=
p
5
> 0 ⇒cos(
á
(SBC),(SCD)) =
p
5
□
Bài 1.7. Cho hình chóp S.ABCD có đáy ABCD là hình vuông . Mặt bên SAB là tam giác
cân tại S, mặt phẳng (SAB) vuông góc với đáy, mặt phẳng (SCD) tạo với đáy góc 600 và cách
đường thẳng AB một khoảng là a. Tính thểtích khối chóp S.ABCD theo a.
Giải:
http://boxmath.vn/

### [Trang 5 - [HÌNH HỌC KHÔNG GIAN 3D]]
A
B
C
D
H
I
S
K
Gọi H, I lần lượt là trung điểm AB và CD Do SAB cân tại S nên SH ⊥AB mà (SAB) ⊥(ABCD)
do đó SH ⊥(ABCD) ⇒SH ⊥CD,HI ⊥CD nên CD ⊥(SHI), kẻHK ⊥SI,CD ⊥HK nên HK ⊥
(SCD) ⇒HK = d(H,(SCD)) = d(AB,(SCD)) = a
CD ⊥(SHI) ⇒
HI⊥CD
SI⊥CD
CD = (SCD)∩(ABCD)







⇒(
á
(SCD),(ABCD) = ( à
HI,SI) = 
SIH = 600
Trong ∆HK I có HI =
HK
sin600 = 2a
p
= BC. Trong ∆HSI có SH = HI.tan600 = 2a
diện tích ABCD là SABCD = BC2 = 4a2
Thểtích S.ABCD là VS.ABCD = 1
3SH.SABCD = 8a3
9 .
□
Bài 1.8. Cho hình chóp S.ABCD có đáy ABCD là hình bình hành thỏa mãn AB = 2a, BC =
a
p
2, BD = a
p
6. Hình chiếu vuông góc của đỉnh S lên mặt phẳng (ABCD) là trọng tâm của
tam giác BCD. Tính theo α thểtích khối chóp S.ABCD, biết rằng khoảng cách giữa hai đường
thẳng AC và SB bằng a.
Giải:
D
C
A
B
O
M
H
S
K
Gọi H là hình chiếu vuông góc của S lên mặt phẳng (ABCD),M là trung điểm CD và O là tâm
của đáy ABCD. Do AO là trung tuyến của tam giác ABD nên AO2 = AB2 + AD2
−BD2
= 3a2
⇒
AO = a
p
2
⇒AH = AO + AO
= 2a
p
3
BM2 = BD2 +BC2
−CD2
= 6a2 +2a2
−4a2
= 3a2 ⇒BM = a
p
3 ⇒BH = 2a
p
3
http://boxmath.vn/

### [Trang 6 - [HÌNH HỌC KHÔNG GIAN 3D]]
Ta có AH2+BH2 = 4a2 = AB2 ⇒AH⊥BH, kết hợp với AH vuông góc với SH ta được AH ⊥(SHB).
KẻHK vuông góc với SB, theo chứng minh trên ta được AH ⊥(SHB) suy ra AH ⊥HK ⇒HK
là đoạn vuông góc chung của AC và SB suy ra HK = a.
Trong tam giác vuông SHB ta có
HK2 =
SH2 +
HB2 ⇒SH = 2a
Ta có VS.ABCD = 1
3SH.SABCD = 1
3SH.4.SOAB = 4
3SH.1
2OA.BH = 4
p
2a3
□
- Khối lăng trụ
Bài 2.1. Cho khối lăng trụtam giác ABC.A1B1C1 có đáy là tam giác đều cạnh 2a, điểm A1
cách đều ba điểm A,B,C. Cạnh bên A1A tạo với mặt phẳng đáy một góc α. Hãy tìm α , biết
thểtích khối lăng trụABC.A1B1C1 bằng 2
p
3a3.
Giải:
A
B
C
I
H
G
A1
B1
C1
Ta có tam giác ABC đều cạnh 2a nên SABC = a2p
Mặt khác A1A = A1B = A1C ⇒A1.ABC là hình chóp tam giác đều đỉnh A1.
Gọi G là trọng tâm tam giác ABC, ta có A1G là đường cao.
Trong tam giác ABC có AG = 2
3 AH = 2a
p
3
Trong tam giác vuông A1AG có: à
A1AG = α; A1G = AG.tanα = 2a
p
3
.tanα.
Thểtích khối lăng trụV = A1G.SABC = 2
p
3a3 ⇒tanα =
p
3 ⇒α = 60o.
□
Bài 2.2. Cho lăng trụđứng ABC.A′B′C′ có đáy ABC là tam giác cân với AB = AC = a, góc

BAC = 1200 , cạnh bên BB′ = a . Gọi I là trung điểm của CC′. Chứng minh tam giác AB′I
vuông tại A và tính cosin của góc giữa hai mặt phẳng (ABC) và (AB′I).
Giải:
http://boxmath.vn/

### [Trang 7 - [HÌNH HỌC KHÔNG GIAN 3D]]
A
B
C
A′
B′
C′
I
Ta có BC = a
p
3. Áp dụng định lí Pitago trong tam giác vuông ACI, ABB′,B′C′I
Suy ra AI =
p
2 a, AB′ =
p
2a,B′I =
p
2
a
Do đó AI2 + AB′2 = B′I2 Vậy tam giác AB′I vuông tại A
SAB′I = 1
2 AI.AB′ =
p
4
a2, SABC =
p
4 a2. Gọi α là góc giữa hai mặt phẳng (ABC) và (AB′I). Tam
giác ABC là hình chiếu vuông góc của tam giác AB′I.
suy ra SA′BI cosα = SABC ⇔
p
4
cosα =
p
4
⇔cosα =
r
10
□
Bài 2.3. (DB1 A 2007) Cho lăng trụđứng ABCA1B1C1 có AB = a, AC = 2a, AA1 = 2a
p
5 và

BAC = 1200. Gọi M là trung điểm của cạnh CC1. Chứng minh MB ⊥MA1 và tính khoảng
cách từđiểm A tới mặt phẳng (A1BM).
Giải:
A
B
C
A1
B1
C1
M
+ Ta có A1M2 = A1C2
1 +C1M2 = 9a2, BC2 = AB2 + AC2 −2AB.AC.cos1200 = 7a2;
BM2 = BC2 +CM2 = 12a2; A1B2 = A1A2 + AB2 = 21a2 = A1M2 + MB2
⇒MB vuông góc với MA1
+ Hình chóp MABA1 và CABA1 có chung đáy là tam giác ABA1 và đường cao bằng nhau nên
thểtích bằng nhau.
⇒V = VMABA1 = VCABA1 = 1
3 AA1.SABC = 1
3a3p
⇒d(a,(MBA1)) =
3V
SMBA1
=
6V
MB.MA1
= a
p
3
□
http://boxmath.vn/

### [Trang 8 - [HÌNH HỌC KHÔNG GIAN 3D]]
Bài 2.4. Cho lăng trụtam giác ABC.A1B1C1 có tất cảcác cạnh bằng a, góc tạo bởi cạnh bên
và mặt đáy bằng 300 . Hình chiếu vuông góc H của đỉnh A trên mặt phẳng (A1B1C1) thuộc
đường thẳng B1C1. Tính thểtích khối lăng trụABC.A1B1C1 và tính khoảng cách giữa hai
đường thẳng AA1 và B1C1 theo a.
Giải:
A1
B1
C1
H
A
C
B
D
à
AA1H = 300, AH = AA1.sin300 = a
Thểtích khối lăng trụABC.A1B1C1: V = AH.dt(A1B1C1) = a3p
8
∆AA1H vuông, A1H = a.cos300 = a
p
2 . Do ∆A1B1C1 đều cạnh a,H thuộc B1C1 và A1H = a
p
2
nên A1H⊥B1C1
Có AH⊥B1C1 do đó B1C1⊥(AA1H). Kẻđường cao HK của ∆AA1H thì HK chính là khoảng cách
giữa AA1 và B1C1
Ta có AA1.HK = AH.A1H, ⇒HK = A1H.AH
AA1
= a
p
4 .
□
Bài 2.5. Cho hình lăng trụABC.A′B′C′ có đáy là tam giác đều cạnh a, hình chiếu vuông góc
của A′ lên mặt phẳng (ABC) trùng với trọng tâm O của tam giác ABC. Một mặt phẳng (P)
chứa BC và vuông góc với AA′, cắt lăng trụtheo một thiết diện có diện tích bằng a2p
8
. Tính
thểtích khối lăng trụABC.A′B′C′ theo a.
Giải:
A
B
C
M
O
A′
B′
C′
H
Gọi M là trung điểm của BC, gọi H là hình chiếu vuông góc của M lên AA′, Khi đó (P) ≡(BCH).
Do góc à
A′AM nhọn nên H nằm giữa AA′. Thiết diện của lăng trụcắt bởi (P) là tam giác BCH.
http://boxmath.vn/

### [Trang 9 - [HÌNH HỌC KHÔNG GIAN 3D]]
Do tam giác ABC đều cạnh a nên AM = a
p
2
, AO = 2
3 AM = a
p
3
Theo bài ra SBCH = a2p
8
⇒1
2HM.BC = a2p
8
⇒HM = a
p
4 ,
AH =
p
AM2 −HM2 =
s
3a2
4 −3a2
16 = 3a
Do hai tam giác A′AO và MAH đồng dạng nên A′O
AO = HM
AH
suy ra A′O = AO.HM
AH
= a
p
3
a
p
4
3a = a
Thểtích khối lăng trụ: V = A′O.SABC = 1
2 A′O.AM.BC = 1
a
a
p
2
a = a3p
12 .
□
- Khối tròn xoay
Bài 3.1. Cho hình trụcó bán kính đáy bằng a và đường cao bằng a
p
2.
a) M và N là hai điểm lưu động trên hai đáy sao cho góc của MN và đáy bằng α . Tính
khoảng cách từtrục đến MN.
b) Tính thểtích và diện tích xung quanh của lăng trụtam giác đều ngọai tiếp hình trụ
Giải:
C
A
B
O
M
N′
O′
A′
B′
C′
N
H
a) Kẻđường sinh NN′ ta có à
NMN′ = α, kẻOH⊥MN′ thì OH bằng khỏang cách giữa trục OO′
và MN.
Ta có: MN′ = NN′.cotα = a.
p
2.cotα
∆OMH vuông : OH2 = OM2 −MH2 = a2 −a2
2 cot2 α = a2
2 (2−cot2 α)
⇒OH = a
s
2−cot2 α
b) Gọi x là cạnh của tam giác đều ngọai tiếp đường tròn đáy của hình trụ.
Ta có: O′N = R = 1
3 AN = 1
x
p
2
= x
p
6
⇒x = 6R
p
= 6a
p
VABC.A′B′C′ = x2p
4
.OO′ = 36a2p
12
.a
p
2 = 3a2.
p
6.
http://boxmath.vn/

### [Trang 10 - [HÌNH HỌC KHÔNG GIAN 3D]]
Sxq = 3x.OO′ = 18a
p
.a
p
2 = 6a2p
6.
□
Bài 3.2. Cho hình nón đỉnh S có đường sinh là a, góc giữa đường sinh và đáy là α .
a) Tính thểtích và diện tích xung quanh của hình nón.
b) Một mặt phẳng hợp với đáy một góc 600 và cắt hình nón theo hai đường sinh SA và SB.
Tính diện tích tam giác SAB và khoảng cách từtâm của đáy hình nón đến mặt phẳng này.
Giải:
O
S
A
B
H
K
a) Tính V và Sxq.
∆SAO vuông : SO = a.sinα, AO = a.cosα
V = 1
3π.AO2.SO = 1
3π.a3.cos2 α.sinα
Sxq = π.AO.SA = π.a2.cosα
b) + Tính SSAB
KẻOH⊥AB ⇒SH⊥AB, do đó 
SOH = 600
∆SOH vuông :OH = SO.cot.600 = a
p
3.sinα
AOH vuông : AH2 = AO2 −OH2 = a2.cos2α−3a2.sinα
⇒AH = a
p
p
3cos2 α−sin2 α
Vậy SSAB = 1
2 AB.SH = 2a2.sinα
p
3cos2 α−sin2 α
+ Tính d(O,(SAB))
KẻOK⊥SH ⇒OK⊥(SAB)
OKH vuông : OK = OH.sin600 = a
p
3sinα
.
p
2 = a.sinα
□
Bài 3.3. Cho hình chóp S.ABCD có đáy ABCD là hình chữnhật và có cạnh bên SA vuông
góc với đáy.
a) Xác định tâm mặt cầu ngọai tiếp hình chóp SABCD.
b) Gọi (P) là mặt phẳng qua A và vuông góc với SC cắt AB,SC,SD lần lượt tại B′,C′,D′.
Chứng tỏrằng bảy điểm A,B,C,D,B′,C′,D′ cùng nằm trên một mặt cầu.
Giải:
http://boxmath.vn/

### [Trang 11 - [HÌNH HỌC KHÔNG GIAN 3D]]
A
B
C
D
S
B′
D′
O
C′
I
a) Ta có :
BC⊥AB
BC⊥SA
)
⇒BC⊥SB
Tương tựCD⊥SD
Vậy các điểm A,B,D đều nhìn đọan SC dưới một góc vuông, do đó tâm mặt cầu ngọai tiếp hình
chóp S.ABCD là trung điểm I của SC.
b)Ta có : AC′⊥SC tại C′ AB′⊥SC và AB′⊥BC ( vì BC⊥(SAB)) nên AB′⊥(SBC) ⇒AB′⊥B′C
Tương tựAD′⊥D′C
Vậy các điểm B′,C′,D′,D,B cùng nhìn đọan AC dưới một góc vuông, do đó bảy điểm A,B,C,D,B′,C′,D′
cùng nằm trên mặt cầu đường kính AC.
□
- Bài tập tựluyện có đáp số
1. (CĐ 2012) Cho khối chóp S.ABC có đáy ABC là tam giác vuông cân tại A, AB = a
p
2,SA =
SB = SC. Góc giữa đường thẳng SA và mặt phẳng (ABC) bằng 600. Tính thểtích khối
chóp S.ABC và bán kính mặt cầu ngoại tiếp hình chóp S.ABC theo a.
* Đáp số: V =
p
3a3
,R = 2a
p
3
2. (D 2012) Cho hình hộp đứng ABCD.A′B′C′D′ có đáy là hình vuông, tam giác A′AC vuông
cân, A′C = a. Tính thểtích của khối tứdiện ABB′C′ và khoảng cách từđiểm A đến mặt
phẳng (BCD′) theo a.
* Đáp số: V = a3p
48 ,d = a
p
6
3. (B 2012) Cho hình chóp tam giác đều S.ABC với SA = 2a, AB = a. Gọi H là hình chiếu
vuông góc của A trên cạnh SC. Chứng minh SC vuông góc với mặt phẳng (ABH). Tính
thểtích của khối chóp S.ABH theo a.
* Đáp số: V = 7
p
11a3
4. (A 2012)Cho hình chóp S.ABC có đáy là tam giác đều cạnh a. Hình chiếu vuông góc của
S trên mặt phẳng (ABC) là điểm H thuộc cạnh AB sao cho HA = 2HB. Góc giữa đường
thẳng SC và mặt phẳng (ABC) bằng 600. Tính thểtích khối chóp S.ABC và tính khoảng
cách giữa hai đường thẳng SA và BC theo a.
* Đáp số: V = a3p
12 , g = a
p
8
http://boxmath.vn/

### [Trang 12 - [HÌNH HỌC KHÔNG GIAN 3D]]
5. (CĐ 2011) Cho hình chóp S.ABC có đáy ABC là tam giác vuông cân tại B, AB = a,SA
vuông góc với mặt phẳng (ABC), góc giữa hai mặt phẳng (SBC) và (ABC) bằng 300. Gọi
M là trung điểm của cạnh SC. Tính thểtích của khối chóp S.ABM theo a.
* Đáp số: V = a3p
36
6. (A 2011) Cho hình chóp S.ABC có đáy ABC là tam giác vuông cân tại B, AB = BC = 2a;
hai mặt phẳng (SAB) và (SAC) cùng vuông góc với mặt phẳng (ABC). Gọi M là trung
điểm của AB; mặt phẳng qua SM và song song với BC, cắt AC tại N. Biết góc giữa hai
mặt phẳng (SBC) và (ABC) bằng 600. Tính thểtích khối chóp S.BCNM và khoảng cách
giữa hai đường thẳng AB và SN theo a.
* Đáp số: V = a3p
3,d = 2a
p
13
7. (B 2011) Cho hình lăng trụABCD.A1B1C1D1 có đáy ABCD là hình chữnhật, AB =
a, AD = a
p
3. Hình chiếu vuông góc của điểm A1 trên mặt phẳng (ABCD) trùng với giao
điểm của AC và BD. Góc giữa hai mặt phẳng (ADD1A1) và (ABCD) bằng 600. Tính thể
tích khối lăng trụđã cho và khoảng cách từđiểm B1 đến mặt phẳng (A1BD) theo a.
* Đáp số: V = 3a3
2 ,d = a
p
2
8. (D 2011) Cho hình chóp S.ABC có đáy ABC là tam giác vuông tại B, BA = 3a,BC = 4a;
mặt phẳng (SBC) vuông góc với mặt phẳng (ABC). Biết SB = 2a
p
3 và 
SBC = 300. Tính
thểtích khối chóp S.ABC và khoảng cách từđiểm B đến mặt phẳng (SAC) theo a.
* Đáp số: V = 2
p
3a3,d = 6a
p
7
9. (A 2010) Cho hình chóp S.ABCD có đáy ABCD là hình vuông cạnh a. Gọi M và N lần
lượt là trung điểm của các cạnh AB và AD; H là giao điểm của CN với DM. Biết SH
vuông góc với mặt phẳng (ABCD) và SH = a
p
3. Tính thểtích khối chóp S.CDNM và tính
khoảng cách giữa hai đường thẳng DM và SC theo a.
* Đáp số: V = 5
p
3a3
,d = 2
p
3a
p
10. (D 2010) Cho hình chóp S.ABCD có đáy ABCD là hình vuông cạnh a, cạnh bên SA = a;
hình chiếu vuông góc của đỉnh S trên mặt phẳng (ABCD) là điểm H thuộc đoạn AC, AH =
AC
4 . Gọi CM là đường cao của tam giác SAC. Chứng minh M là trung điểm của SA và
tính thểtích khối tứdiện SMBC theo a.
* Đáp số: V = a3p
48
11. (CĐ 2010) Cho hình chóp S.ABCD có đáy ABCD là hình vuông cạnh a, mặt
phẳng (SAB) vuông góc với mặt phẳng đáy, SA = SB, góc giữa đường thẳng
SC và mặt phẳng đáy bằng 450. Tính theo a thểtích khối chóp S.ABCD.
* Đáp số: a3p
6
12. (B 2010) Cho lăng trụtam giác đều ABC.A′B′C′ có AB = a, góc giữa hai mặt
phẳng (A′BC) và (ABC) bằng 600. Gọi G là trọng tâm tam giác A′BC. Tính
thểtích khối lăng trụđã cho và tính bán kính mặt cầu ngoại tiếp tứdiện GABC theo a.
* Đáp số: V = 3a3p
8
,R = 7a
http://boxmath.vn/

### [Trang 13 - [HÌNH HỌC KHÔNG GIAN 3D]]
13. (CĐ 2009) Cho hình chóp tứgiác đều S.ABCD có AB = a,SA = a
p
2. Gọi M,N và P lần
lượt là trung điểm của các cạnh SA,SB và CD. Chứng minh đường thẳng MN vuông góc
với đường thẳng SP. Tính theo a thểtích khối tứdiện AMNP.
* Đáp số: V = a3p
48
14. (A 2009) Cho hình chóp S.ABCD có đáy ABCD là hình thang vuông tại A và D; AB =
AD = 2a,CD = a; góc giữa hai mặt phẳng (SBC) và (ABCD) bằng 600. Gọi I là trung điểm
của cạnh AD. Biết hai mặt phẳng (SBI) và (CSI) cùng vuông góc với mặt phẳng (ABCD),
tính thểtích khối chóp S.ABCD theo a.
* Đáp số: V = 3
p
15a3
15. (B 2009) Cho hình lăng trụtam giác ABC.A′B′C′ có BB′ = a, góc giữa đường thẳng BB′ và
mặt phẳng (ABC) bằng 600; tam giác ABC vuông tại C và 
BAC = 600. Hình chiếu vuông
góc của điểm B′ lên mặt phẳng (ABC) trùng với trọng tâm của tam giác ABC. Tính thể
tích khối tứdiện A′ABC theo a.
* Đáp số: V = 9a3
16. (D 2009) Cho hình lăng trụđứng ABC.A′B′C′ có đáy ABC là tam giác vuông tại B,
AB = a, AA′ = 2a, A′C = 3a. Gọi M là trung điểm của đoạn thẳng A′C′, I là giao điểm của
AM và A′C. Tính theo a thểtích khối tứdiện IABC và khoảng cách từđiểm A đến mặt
phẳng (IBC).
* Đáp số: V = 4a3
9 ,d = 2a
p
5
17. (CĐ 2008) Cho hình chóp S.ABCD có đáy ABCD là hình thang, 
BAD = 
ABC = 900, AB =
BC = a, AD = 2a,SA vuông góc với đáy và SA = 2a. Gọi M,N lần lượt là trung điểm
của SA,SD. Chứng minh rằng BCNM là hình chữnhật và tính thểtích của khối chóp
S.BCNM theo a.
* Đáp số: V = a3
18. (A 2008) Cho lăng trụABC.A′B′C′ có độdài cạnh bên bằng 2a, đáy ABC là tam giác
vuông tại A, AB = a, AC = a
p
3 và hình chiếu vuông góc của đỉnh A′ trên mặt phẳng
(ABC) là trung điểm của cạnh BC. Tính theo a thểtích khối chóp A′.ABC và tính cosin
của góc giữa hai đường thẳng AA′,B′C′.
* Đáp số: V = a3
2 , cosϕ = 1
19. (B 2008) Cho hình chóp S.ABCD có đáy ABCD là hình vuông cạnh 2a,SA = a,SB = a
p
và mặt phẳng (SAB) vuông góc với mặt phẳng đáy. Gọi M,N lần lượt là trung điểm của
các cạnh AB,BC. Tính theo a thểtích khối chóp S.BMDN và tính cosin của góc giữa hai
đường thẳng SM,DN.
* Đáp số: V = a3p
3
, cosϕ =
p
5
20. (D 2008) Cho lăng trụđứng ABC.A′B′C′ có đáy ABC là tam giác vuông, AB = BC = a,
cạnh bên AA′ = a
p
2. Gọi M là trung điểm của cạnh BC. Tính theo a thểtích của khối
http://boxmath.vn/

### [Trang 14 - [HÌNH HỌC KHÔNG GIAN 3D]]
lăng trụABC.A′B′C′ và khoảng cách giữa hai đường thẳng AM,B′C.
* Đáp số: V = a3p
2
,d =
p
7a
21. (A 2007) Cho hình chóp S.ABCD có đáy là hình vuông cạnh a, mặt bên SAD là tam giác
đều và nằm trong mặt phẳng vuông góc với đáy. Gọi M,N,P lần lượt là trung điểm của
các cạnh SB,BC,CD. Chứng minh AM vuông góc với BP và tính thểtích của khối tứdiện
CMNP.
* Đáp số: V =
p
3a3
22. (B 2007) Cho hình chóp tứgiác đều S.ABCD có đáy là hình vuông cạnh a. Gọi E là điểm
đối xứng của D qua trung điểm của SA,M là trung điểm của AE,N là trung điểm của
BC. Chứng minh MN vuông góc với BD và tính theo a khoảng cách giữa hai đường thẳng
MN và AC.
* Đáp số: d = a
p
4
23. (D 2007) Cho hình chóp S.ABCD có đáy là hình thang, 
ABC = 
BAD = 900,BA = BC =
a, AD = 2a. Cạnh bên SA vuông góc với đáy và SA = a
p
2. Gọi H là hình chiếu vuông góc
của A trên SB. Chứng minh tam giác SCD vuông và tính theo a khoảng cách từH đến
mặt phẳng (SCD).
* Đáp số: d = a
24. (A 2006) Cho hình trụcó đáy là hai hình tròn tâm O và O′, bán kính đáy bằng
chiều cao và bằng a. Trên đường tròn đáy tâm O lấy điểm A, trên đường tròn
đáy tâm O′ lấy điểm B sao cho AB = 2a. Tính thểtích của khối tứdiện OO′AB.
* Đáp số: V =
p
3a3
25. (B 2006) cho hình chóp S.ABCD có đáy ABCD là hình chữnhật với AB = a,
AD = a
p
2,SA = a và SA vuông góc với mặt phẳng (ABCD). Gọi M và N lần
lượt là trung điểm của AD và SC; I là giao điểm của BM và AC. Chứng minh
mặt phẳng (SAC) vuông góc với mặt phẳng (SMB). Tính thểtích của khối tứdiện ANIB.
* Đáp số: V =
p
2a3
26. (D 2006) Cho hình chóp tam giác S.ABC có đáy ABC là tam giác đều cạnh a,SA = 2a và
SA vuông góc với mặt phẳng (ABC). Gọi M và N lần lượt là hình chiếu vuông góc của A
trên các đường thẳng SB và SC. Tính thểtích của khối chóp A.BCNM.
* Đáp số: V = 3
p
3a3
27. (B 2004) Cho hình chóp tứgiác đều S.ABCD có cạnh đáy bằng a, góc giữa cạnh bên và
mặt đáy bằng ϕ((00 < ϕ < 900). Tính tang của góc giữa hai mặt phẳng (SAB) và (ABCD)
theo ϕ. Tính thểtích khối chóp S.ABCD theo a và ϕ.
* Đáp số: tanα =
p
2tanϕ,V =
p
2a3tanϕ
28. (D 2003) Cho hai mặt phẳng (P) và (Q) vuông góc với nhau, có giao tuyến là đường thẳng
∆. Trên ∆lấy hai điểm A,B với AB = a. Trong mặt phẳng (P) lấy điểm C, trong mặt
http://boxmath.vn/

### [Trang 15 - [HÌNH HỌC KHÔNG GIAN 3D]]
phẳng (Q) lấy điểm D sao cho AC,BD cùng vuông góc với ∆và AC = BD = AB. Tính bán
kính mặt cầu ngoại tiếp tứdiện ABCD và tính khoảng cách từA đến mặt phẳng (BCD)
theo a.
* Đáp số: R = a
p
2
,d = a
p
2
29. (B 2002) Cho hình lập phương ABCD.A1B1C1D1 có cạnh bằng a. a) Tính theo a khoảng
cách giữa hai đường thẳng A1B và B1D. b) Gọi M,N,P lần lượt là các trung điểm của các
cạnh BB1,CD, A1D1. Tính góc giữa hai đường thẳng MP và C1N.
* Đáp số: d = a
p
, g = 900
30. (D 2002) Cho hình tứdiện ABCD có AD vuông góc với mặt phẳng (ABC); AC = AD =
4cm; AB = 3cm;BC = 5cm. Tính khoảng cách từđiểm A tới mặt phẳng (BCD).
* Đáp số: d = 6
p
17
31. (DB1 A 2007) Cho lăng trụđứng ABCA1B1C1 có AB = a, AC = 2a, AA1 = 2a
p
5 và 
BAC =
1200. Gọi M là trung điểm của cạnh CC1. Chứng minh MB ⊥MA1 và tính khoảng cách
từđiểm A tới mặt phẳng (A1BM).
* Đáp số: d = a
p
3
32. (DB2 A 2007) Cho hình chóp S.ABC có góc giữa hai mặt phẳng (SBC) và (ABC) bằng
600, hai tam giác ABC và SBC là các tam giác đều cạnh a. Tính theo a khoảng cách từB
đến mặt phẳng (SAC).
* Đáp số: d = 3a
p
33. (DB1 B 2007) Cho hình chóp S.ABCD có đáy ABCD là hình vuông tâm O, SA vuông
góc với đáy. Cho AB = a,SA = a
p
2. Gọi H và K lần lượt là hình chiếu của A lên SB,SD.
Chứng minh SC ⊥(AHK) và tính thểtích khối chóp OAHK.
* Đáp số: V = 2a3
34. (DB2 B 2007) Trong mặt phẳng (P) cho nửa đường tròn đường kính AB = 2R và điểm C
thuộc nửa đường tròn đó sao cho AC = R. Trên đường thẳng vuông góc với (P) tại A lấy
điểm S sao cho góc giữa hai mặt phẳng (SAB) và (SBC) bằng 600. Gọi H,K lần lượt là
hình chiếu vuông góc của A trên SB,SC. Chứng minh tam giác AHK vuông và tính thể
tích khối tứdiện SABC theo R.
* Đáp số: V = R3p
12
35. (DB1 D 2007) Cho lăng trụđứng ABC.A1B1C1 có đáy ABC là tam giác vuông AB = AC =
a, AA1 = a
p
2. Gọi M,N lần lượt là trung điểm của AA1,BC1. Chứng minh MN là đường
vuông góc chung của các đường thẳng AA1 và BC1. Tính thểtích khối tứdiện MA1BC1.
* Đáp số: V = a3p
12
36. (DB2 D 2007) Cho lăng trụđứng ABCA1B1C1 có tất cảcác cạnh đều bằng a. M là trung
điểm của AA1. Chứng minh BM ⊥B1C và tính khoảng cách giữa hai đường thẳng BM
http://boxmath.vn/


------------------------------------------------------------

## NGUỒN: VIETNAM IMO BOOKLET 2017-22 (-20)
- **Phân hệ:** [HÌNH HỌC PHẲNG OLYMPIC 2D]
- **Tên file:** `Vietnam IMO Booklet 2017-22 (-20).pdf` (213 trang)

### [Trang 2 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Vietnamese Mathematical Competitions 2017
Vietnamese Ministry of Training and Education
VIETNAMESE
Mathematical Competitions
for high school students
VMC 2017
Hanoi, July 2017

### [Trang 4 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Vietnamese Mathematical Competitions 2017
Table of Contents
Vietnamese Mathematical Olympiad 2017
1.1
Day 1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
1.2
Day 2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
Vietnamese Team Selection Test for IMO 2017
2.1
Day 1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
2.2
Day 2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
Solution of VMO 2017
4
Solution of Vietnam TST for IMO 2017

### [Trang 6 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Vietnamese Mathematical Competitions 2017
Preface
The Vietnam Mathematical Olympiad 2017 for high school students took
place in all cities of Vietnam on 05-06th January, 2017. After that com-
petition, a two-day IMO Team selection test was organized. The top 48
students and one student who got a Silver medal at IMO 2016 took two
tests on 25th and 26th of March.
Based on the TST result, the Vietnamese team for the 58th International
Mathematical Olympiad 2017 in Rio de Janeiro, Brazil were selected:
1. Phan Nhat Duy
2. Le Quang Dung
3. Nguyen Canh Hoang
4. Hoang Huu Quoc Huy
5. Pham Nam Khanh
6. Do Van Quyet
Dr. Le Anh Vinh (The Vietnam Institute of Educational Sciences - Hanoi)
and Dr. Le Ba Khanh Trinh (Vietnam National University - Ho Chi Minh
city) were appointed as the Leader and the Deputy Leader of the Viet-
namese IMO team 2017. The team is also accompanied by Mr. Nguyen
Khac Minh (Ministry of Education and Training). This booklet, includes
problems and solutions of VMO and TST this year, which was edited by
Le Phuc Lu (FPT Software Ho Chi Minh City), Nguyen Van Quy (Hanoi
University of Science). We also say thanks to the trainers help us in com-
pletion the booklet: Dr. Tran Nam Dung, Vo Quoc Ba Can, Tran Quang
Hung, Nguyen Van Linh, Nguyen Huy Tung, Luong Van Khai.

### [Trang 7 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Vietnamese Mathematical Competitions 2017
The Vietnamese team at IMO 2017
Phan Nhat Duy
Le Quang Dung
Nguyen Canh Hoang
Hoang Huu Quoc Huy
Pham Nam Khanh
Do Van Quyet
Team Training Administrators
Le Ba Khanh Trinh
Le Anh Vinh
Nguyen Khac Minh

### [Trang 8 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Vietnamese Mathematical Competitions 2017
Problems from the contests
Vietnamese Mathematical Olympiad 2017
1.1
Day 1
Problem
1.
Given a real number a and consider the sequence (un)
deﬁned by
u1 = a,
un+1 = 1
2 +
s
2n+3
n+1 un + 1
4,
∀n ∈N∗.
1. If a = 5, prove that (un) has a ﬁnite limit and ﬁnds that limit.
2. Find all the values of a such that the sequence (un) deﬁnes and has
ﬁnite limits.
Problem 2.
Does there exist a polynomial P(x) with integer coeﬃcients
such that P

1+ 3√

= 1+ 3√
2 and P

1+
√

= 2+3
√
5?
Problem 3.
Let ABC be an acute, non isosceles triangle with (O) is its
circumcircle. Denote H as the orthocenter and BE,CF as the altitudes
of triangle ABC. Suppose that AH intersects (O) at D diﬀers from A.
1. Let I be the midpoint of AH, EI meets BD at M and FI meets
CD at N. Prove that MN is perpendicular to OH.
2. The lines DE,DF intersect (O) at P,Q respectively (P and Q are
diﬀer from D). The circle (AEF) intersects (O) and AO at R,S
respectively (R and S diﬀer from A). Prove that BP,CQ,RS are
concurrent.

### [Trang 9 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Vietnamese Mathematical Competitions 2017
Problem
4.
Let n be a positive integer and n > 1. The square table
ABCD of size n consists of n2 unit cells, each of them is colored by one
of three colors: black, white, gray. A way to color this table is called
"nice" if each cell on the diagonal AC is colored by gray and each pair of
cells that symmetric respect to AC are colored by the same color, both
white or both black. One can ﬁll in each gray cell by the number 0, each
black cell by negative integer and each white cell by positive integer. For
each positive integer k, a way to ﬁll in the table is called "k-balanced" if
it satisﬁes all following conditions:
• All cells of the table are ﬁlled by the integers belong to the segment
[−k;k].
• If a row meets a column at a black cell then the sets of positive
integers on that row and that column are disjoint. Similarly, if a
row meets a column at a white cell then the sets of negative integers
on that row and that column are disjoint.
1. For n = 5, ﬁnd the minimum value of k such that there exists a
k-balanced way to ﬁll in the table below.
2. For n = 2017, ﬁnd the minimum value of k such that for all nice way
to color the table, we can ﬁll in the table by k-balanced way.
1.2
Day 2
Problem 5.
Find all functions f : R →R such that
f

xf(y)−f(x)

= 2f(x)+xy
for all real numbers x, y.
Problem 6.
Show that

### [Trang 10 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Vietnamese Mathematical Competitions 2017
2. VIETNAMESE TEAM SELECTION TEST FOR IMO 2017
a)
X
k=1
kCk
2017 ≡0 (mod 20172).
b)
X
k=1
(−1)kCk
2017 ≡3(22016 −1) (mod 20172).
Problem 7.
Let ABC be an acute triangle inscribed in the circle (O)
and I is the circumcenter of triangle OBC. The point G belongs to the
arc BC (not contains O) of (I). The circle (ABG) intersects AC at E
and circle ACG intersects AB at F (points E,F diﬀer from A).
1. Denote K as the intersection of BE and CF. Prove that AK,BC
and OG are concurrent.
2. Let D be a ﬁxed point on the arc BC that contains O of (I) and GB
meets CD at M, GC meets BD at N. Suppose that MN intersects
(O) at P,Q Prove that when G moves on (I), the circumcircle of
triangle GPQ always pass through two certain ﬁxed points.
Vietnamese Team Selection Test for IMO 2017
2.1
Day 1
Problem 1.
There are 44 distinct holes on a line and 2017 ants. Each
ant crawled up from a hole, then moved to another hole and crawled down.
Denote T as the set of time points that the ants crawled up or crawled
down from some hole. Suppose that the speed of the ants are pairwise
distinct and they did not change its speed. Prove that if |T| ≤45 then
there exist two ants did not meet. Note that two ants met when there
exist a time point such that they were at the same location on the line,
including the holes.
Problem 2.
For every positive integer n, let xn = Cn
2n.
1. Show that if 2017k
< n < 2017k for some positive integer k then xn
is a multiple of 2017.
2. Find all positive integer h > 1 such that there exist positive integers
N,T such that for all n > N then (xn) is a periodic sequence mod h
with period T.
Problem
3.
Let ABC be a triangle with I is its incenter and the
circle (I) is tangent to BC,CA,AB at D,E,F respectively. Denote Ib,Ic
as the excenters of triangle ABC respect to vertices B,C. Let P,Q be the

### [Trang 11 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Vietnamese Mathematical Competitions 2017
midpoints of segments IbE,IcF. Suppose that (PAC) intersects AB at
the second point R and (QAB) intersects AC at the second point S.
1. Prove that PR,QS,AI are concurrent.
2. Suppose that DE,DF intersect IbIc at K,J and EJ meets FK at
M. The lines PE,QF intersect (PAC),(QAB) at X,Y (X diﬀers
from P and Y diﬀers from Q). Prove that BY,CX and AM are
concurrent.
2.2
Day 2
Problem 4.
Let B,C be two ﬁxed points on the ﬁxed circle (O) (BC is
not the diameter of (O)). The points A moves on (O) such that AB > BC
and M is the midpoint of AC. The circle of diameter BM intersects (O)
at R. Suppose that RM intersects (O) at the second point Q and cut BC
at P. The circle of diameter BP intersects AB,BO at the second points
K,S respectively.
1. Prove that SR passes through the midpoint of KP.
2. Denote N as the midpoint of BC. The radical axis of two circles of
diameter AN,BM intersects SR at E. Prove that ME always pass
through the certain ﬁxed point when A moves on (O).
Problem
5.
Given 2017 positive real numbers a1, a2, ..., a2017. For
each positive integer n > 2017, let
an = max
n
ai1ai2ai3 |i1 +i2 +i3 = n, 1 ≤i1 ≤i2 ≤i3 ≤n−1
o
.
Prove there exists some positive integers m ≤2017 and N > 4m such that
anan−4m = a2
n−2m for every n > N.
Problem
6.
For a positive integer n, consider a1,a2,...,a2n as a
permutation of the ﬁrst 2n positive integers.
A permutation is called
"nice" if ai +an+i = 2n+1,i = 1,2,3,...,n and ai −ai+1 is not congruent
to aj −aj+1 modulo 2n+1 for all 1 ≤i < j ≤2n (suppose that a2n+1 = a1).
1. For n = 6, give an example of the nice permutation.
2. Prove that for all n, there alway exist some nice permutation.

### [Trang 12 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Vietnamese Mathematical Competitions 2017
Solution for the tests
Solution of VMO 2017
Given a real number a and consider the sequence (un) deﬁned by
u1 = a,
un+1 = 1
2 +
s
2n+3
n+1 un + 1
4,
∀n ∈N∗.
1. If a = 5, prove that (un) has a ﬁnite limit and ﬁnds that limit.
2. Find all the values of a such that the sequence (un) deﬁnes and
has ﬁnite limits.
Problem 1
Solution
We will solve directly part 2), from which to deduce the result of part
1). It can be seen that the sequence (un) deﬁnes if and only if u2 deﬁnes.
Since u2 = 1
2 +
q
2a+ 1
4, then u2 deﬁnes if and only if
a ≥−1
10.
We will prove that the sequence (un) converges to 3 for every a ≥−1
10.
It is easy to see that un ≥1
2, ∀n ≥2. Note that f(x) = 2x+3
x+1 is a strictly
decreasing function over R+ so for every positive integers n, we have
2n+3
n+1 > 2(n+1)+3
(n+1)+1 .

### [Trang 13 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Vietnamese Mathematical Competitions 2017
If there exists a number n0 ∈N such that un0 ≥un0+1 then we have
un0+2 = 1
2 +
v
u
u
t2(n0 +1)+3
(n0 +1)+1 un0+1 + 1
4 ≤1
2 +
s
2n0 +3
n0 +1 un0 + 1
4 = un0+1.
Similarly, we have un0 ≥un0+1 ≥un0+2 ≥un0+3 ≥··· This means that
the sequence (un) does not increase from n0 onward.
Simultaneously,
the sequence is also bounded lower for every n ≥2 so there exists limit
limun = L

L ≥1

. Now, convert equation (1) to limit, we get
L = 1
2 +
s
2L+ 1
4.
Solve this equation, we have L = 3. In summary, if there exists n0 as above
then limun = 3.
Next, we consider the case: the number n0 as above does not exist, in
other words the sequence (un) is strictly decreasing. We will prove (un)
is also bounded above. Indeed, since un+1 > un and 2n+3
n+1 < 3 for every
n ≥2 so we have
2 +
s
3un + 1
4 > 1
2 +
s
2n+3
n+1 un + 1
4 = un+1 > un,
∀n ≥2.
Solving this inequation of un, we have un < 4+
√
2
for every n ≥2. There-
fore the sequence (un) is strictly decreasing and bounded upper by 4+
√
2
so it has a ﬁnite limit. Hence, by convert equation (1) to limit, we also
have limun = 3.
In summary, for every a ≥−1
10 the sequence (un) deﬁnes and converges
to 3.
■
Does there exist a polynomial P(x) with integer coeﬃcients such that
P

1+
3√

= 1+
3√
and
P

1+
√

= 2+3
√
5?
Problem 2
Solution
Suppose that there exists such polynomial P(x). Let Q(x) = P(1+x)−1
then Q(x) ∈Z[x]. We have Q

3√

=
3√
2 and Q
√

= 1+3
√
5.

### [Trang 14 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Vietnamese Mathematical Competitions 2017
3. SOLUTION OF VMO 2017
Therefore, Q(x)−x has an irrational root
3√
2. Since x3 −2 is irreducible
over Z[x] and has the same root
3√
2, we get x3 −2 | Q(x)−x. Then there
exists R(x) with integer coeﬃcients such that
Q(x)−x = (x3 −2)R(x).
Because R(x) ∈Z[x] so R
√

= a + b
√
5 for some a, b ∈Z. Let x =
√
then:
1+3
√
5 =

√
5−2

a+b
√

= 25b−2a+(5a−2b)
√
5,
This implies 5a −2b = 3 and 2a = 25b −1, which has not a pair integer
(a,b) satisfying, a contradictions. So the answer is no.
■
Let ABC be an acute, non isosceles triangle with (O) is its circum-
circle. Denote H as the orthocenter and BE,CF as the altitudes of
triangle ABC. Suppose that AH intersects (O) at D diﬀers from A.
1. Let I be the midpoint of AH, EI meets BD at M and FI meets
CD at N. Prove that MN is perpendicular to OH.
2. The lines DE,DF intersect (O) at P,Q respectively (P and Q
diﬀer from D). The circle (AEF) intersects (O) and AO at R,S
respectively (R and S diﬀer from A). Prove that BP,CQ,RS
are concurrent.
Problem 3
Solution
1) Denote J as the center of nine points circle of triangle ABC then (J)
passes through E, I, F and the point J is also the midpoint of segment
OH. It is easy to see that D and H are symmetric with respect to the
line BC then triangle BDH is isosceles with BD = BH. Since triangle
IEH has IE = IH then
∠IEH = ∠IHE = ∠BHD = ∠BDH,
which implies that BDEI is a cyclic quadrilateral. But DB cuts EI at
M then
ME ·MI = MB ·MD.

### [Trang 15 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Vietnamese Mathematical Competitions 2017
A
B
C
O
H
I
E
F
D
M
N
J
Thus the power of the point M to circles (J) and (O) are equal. Similarly,
the power of the point N to circles (J) and (O) are also equal. So we can
conclude that MN is the radical axis of (O) and (J), thus MN ⊥OJ.
But O,H,J are collinear then MN ⊥OH.
2) Let X be the midpoint of EF and K be the intersection of AH and
BC.
It is easy to see that two triangles BFE and KHE are similar,
which implies that two triangle BFX and DHE are also similar, thus
∠FBX = ∠HDE = ∠FBP.
Then three points B, X, P are collinear;
similar to three points C, X, Q.
A
B
C
O
H
K
F
E
I
D
P
Q
X
S
L
R
M

### [Trang 16 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Vietnamese Mathematical Competitions 2017
3. SOLUTION OF VMO 2017
Denote AL as the diameter of circle (O) then we can see that SH passes
through L and quadrilateral HBLC is a parallelogram, which implies that
HL passes through the midpoint M of BC. It is easy to check that two
triangle SEC and SFB are similar then two triangle SEF and SCB are
also similar. These triangles have the medians SX and SM respectively
then ∠FSX = ∠BSM. We also have two triangles SFB and SRL are
similar then two triangles SFR and SBL are also similar. Thus
∠FSR = ∠BSL = ∠BSM = ∠FSX.
From this we can conclude that three points S, X, R are collinear or SR
passes through X. Therefore, three lines BP, CQ and RS are concurrent
at the midpoint X of the segment EF.
■
Let n be a positive integer and n > 1. The square table ABCD of
size n consists of n2 unit cells, each of them is colored by one of three
colors: black, white, gray. A way to color this table is called "nice" if
each cell on the diagonal AC is colored by gray and each pair of cells
that symmetric respect to AC are colored by the same color, both
white or both black. One can ﬁll in each gray cell by the number
0, each black cell by negative integer and each white cell by positive
integer. For each positive integer k, a way to ﬁll in the table is called
"k-balanced" if it satisﬁes all following conditions:
• All cells of the table are ﬁlled by the integers belong to the
segment [−k;k].
• If a row meets a column at a black cell then the sets of positive
integers on that row and that column are disjoint. Similarly, if
a row meets a column at a white cell then the sets of negative
integers on that row and that column are disjoint.
1. For n = 5, ﬁnd the minimum value of k such that there exists a
k-balanced way to ﬁll in the table below.
2. For n = 2017, ﬁnd the minimum value of k such that for all nice
way to color the table, we can ﬁll in the table by k-balanced
way.
Problem 4
Solution

### [Trang 17 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Vietnamese Mathematical Competitions 2017
1) Let a,b,c be the number ﬁll on the cells at position (1;2),(2;1) and
(3;4),(4;3) and (4;5),(5;4). It is easy to check that all a,b,c must pairwise
distinct, then k ≥3.
We have the way to ﬁll in the table with k = 3 as follows:
Thus the minimum value of k in this case is 3.
2) First, consider the nice coloring way as the chessboard in which the cell
(i,j) colored by black if and only if i+j is even.
Take two white positions on the table at location (a, b) and (c, d), 1 ≤
a, b, c, d ≤2017.
• If a+c is even then b+d is also even, which implies that a+d and
b + c are both odd. Then, one of two cells (a, d) and (b, c) will be
colored by black since they cannot lie on the diagonal AC. Thus the
numbers ﬁlled in white cells are diﬀerent.
• If a+c is odd then b+d is also odd, consider cell (d, c) while ﬁlled in
by the same number as (c, d) then we can apply the same argument
as above to conclude that the numbers ﬁlled in the white cells are
diﬀerent.

### [Trang 18 - [HÌNH HỌC PHẲNG OLYMPIC 2D]]
Vietnamese Mathematical Competitions 2017
3. SOLUTION OF VMO 2017
Hence, all positive numbers on the right upper of the table are pairwise
distinct. This implies that
k ≥2+4+6+···+2016 = 1008·1009 = 20172 −1
.
We shall prove that for all symmetric coloring ways, one can use at most
4
positive integers to ﬁll in the board which satisfy the given conditions
(the argument is the same for negative integers).
Consider the graph of 2017 vertices, namely A1,A2,...,A2017. If row i and
column j intersect at a white cell which ﬁlled in by a number a > 0, then
we connect AiAj and call a as the weight of this edge. This graph is well
deﬁned since the symmetric properties and from the given condition, we
can conclude that: two arbitrary vertices that not connected belongs to
edges of diﬀerent weights. We have to show that for all graph of n > 1
vertices, there is a way to assign at most n2
4 distinct weights to the edges
(∗).
We shall prove (∗) by induction. It is easy to check with n = 1,2,3.
Consider n ≥4 and suppose that the conclusion is true for a graph of n−3
vertices, we consider the graph of n vertices. There are two cases:
1. If the number of edges in the graph is not more than n2
4 then we can
easily assign a unique weight to an edge which satisfy the condition.
If the number of edges in the graph is more than n2
4 then there are
three vertices Ai,Aj,Ak which are pairwise connected. This is true
because from Mantel’s theorem, we already know that: If a graph
has n vertices and more than n2
4 edges then it contains a triangle
(which means three vertices are pairwise connected).
We assign to AiAj,AjAk and AkAi the same weight and assign no
more than n−3 distinct weights to the edges connect between one
of three vertices Ai,Aj,Ak and n −3 other vertices. By applying
induction hypothesis, we can assign at most (n−3)2
distinct weights
to the edges connect among n −3 other vertices. Furthermore, we
have
1+(n−3)+ (n−3)2
≤n2
4 .
This implies that (∗) also holds for n.
For n = 2017, we have

4

= 20172−1
and this is exactly the minimum
value of k.
■


------------------------------------------------------------
