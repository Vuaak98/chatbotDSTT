Bài 1.
(a): Với $a=-1$ thì ma trận $A$ bằng
$$
A=\left(\begin{array}{llll}
1 & 0 & 1 & 0 \\
2 & 1 & 0 & 1 \\
1 & 0 & 1 & 0 \\
0 & 1 & 2 & 1
\end{array}\right)
$$
Hạng của ma trận lúc này bằng 3 .
(b): Dùng biến đổi sơ cấp hàng và khai triển Laplace ta có
$$
\begin{aligned}
\operatorname{det}(A) & =\operatorname{det}\left(\begin{array}{cccc}
1 & a+1 & a+2 & 0 \\
a+3 & 1 & 0 & a+2 \\
0 & a & a+3 & -1 \\
0 & a+2 & a+3 & 1
\end{array}\right) \\
& =\operatorname{det}\left(\begin{array}{ccc}
1 & 0 & a+2 \\
a & a+3 & -1 \\
a+2 & a+3 & 1
\end{array}\right)-(a+3) \operatorname{det}\left(\begin{array}{ccc}
a+1 & a+2 & 0 \\
a & a+3 & -1 \\
a+2 & a+3 & 1
\end{array}\right) \\
& =2(a+3)+(a+2)[a(a+3)-(a+2)(a+3)]- (a+3)[2(a+3)(a+1)-(a+2)(2 a+2)] \\
& =2(a+3)-2(a+2)(a+3)-(a+3)(2 a+2), \\
& =-4(a+1)(a+3) .
\end{aligned}
$$
Do đó định thức $\operatorname{det}(A)>0$ khi và chỉ khi $-3<a<-1$.
(c): Nếu $a \neq-3,-1$, thì $\operatorname{det}(A) \neq 0$. Do đó trong trường hợp này phương trình chỉ có nghiệm tầm thường, số chiều của không gian nghiệm tương ứng bằng 0.  
Với $a \in\{-1,-3\}$, tính cụ thể được $\operatorname{rank}(A)=3$. Số chiều của không gian nghiệm tương ứng bằng $4-\operatorname{rank}(A)=1$.

Bài 2.
(a): Hai ma trận $A, B$ cùng có đa thức đặc trưng là $X^{2}-2$, do đó cùng có giá trị riêng $\pm \sqrt{2}$.
Với $\lambda_{1}=\sqrt{2}$, một vectơ riêng tương ứng của $A$ là $(\sqrt{2}, 1)^{T}$.
Với $\lambda_{2}=-\sqrt{2}$, một vectơ riêng tương ứng của $A$ là $(-\sqrt{2}, 1)^{T}$.
Do đó với
$$
P=\left(\begin{array}{cc}
\sqrt{2} & -\sqrt{2} \\
1 & 1
\end{array}\right)
$$
ta có
$$
P^{-1} A P=\left(\begin{array}{cc}
\sqrt{2} & 0 \\
0 & \sqrt{2}
\end{array}\right)
$$
(b): Điều kiện $R^{-1} A R=B$ tương đương $A R=R B$. Đặt
$$
R=\left(\begin{array}{ll}
a & b \\
c & d
\end{array}\right)
$$
suy ra điều kiện $A R=R B$ trở thành
$$
\left\{\begin{array}{l}
a=-d, \\
b=-2 c .
\end{array}\right.
$$
Do đó tất cả các ma trận $R$ thỏa mãn đề bài là: $R=\left(\begin{array}{cc}a & -2 c \\ c & -a\end{array}\right)$, với $a, b, c, d \in \mathbb{R}$ thỏa mãn $-a^{2}+2 c^{2}=1$. Ví dụ về một ma trận như vậy được cho bởi $R=\left(\begin{array}{ll}1 & -2 \\ 1 & -1\end{array}\right)$.

Bài 3.
(a): Gọi $a_{i}$ là số muỗi ban đầu tương ứng của phòng $i \in\{1,2,3,4\}$. Từ giả thiết ta có hệ phương trình:
$$
\left\{\begin{array}{l}
0.4 a_{1}+0.2 a_{4}=24 \\
0.4 a_{2}+0.3 a_{3}+0.2 a_{4}=50 \\
0.3 a_{2}+0.4 a_{3}+0.2 a_{4}=52 \\
0.6 a_{1}+0.3 a_{2}+0.3 a_{3}+0.4 a_{4}=74
\end{array}\right.
$$
Giải hệ phương trình này ta nhận được nghiệm $\left(a_{1}, a_{2}, a_{3}, a_{4}\right)$ với:
$$
a_{1}=20, a_{2}=40, a_{3}=60, a_{4}=80
$$
Vậy thời điểm ban đầu số muỗi của các phòng lần lượt là $20 ; 40 ; 60 ; 80$.
(b): Gọi $x_{1}, x_{2}, x_{3}, x_{4}$ là số muỗi tương ứng của các phòng $1,2,3,4$ ở trạng thái ổn định. Khi đó $x_{1}+x_{2}+x_{3}+x_{4}=200$, và sau một phút số muỗi mỗi phòng tương ứng sẽ là $x_{1}^{\prime}, x_{2}^{\prime}, x_{3}^{\prime}, x_{4}^{\prime}$ trong đó
$$
\left\{\begin{array}{l}
x_{1}^{\prime}=0.4 x_{1}+0.2 x_{4} \\
x_{2}^{\prime}=0.4 x_{2}+0.3 x_{3}+0.2 x_{4} \\
x_{3}^{\prime}=0.3 x_{2}+0.4 x_{3}+0.2 x_{4} \\
x_{4}^{\prime}=0.6 x_{1}+0.3 x_{2}+0.3 x_{3}+0.4 x_{4}
\end{array}\right.
$$
Từ điều kiện trạng thái ổn định $\left(x_{1}^{\prime}, x_{2}^{\prime}, x_{3}^{\prime}, x_{4}^{\prime}\right)=\left(x_{1}, x_{2}, x_{3}, x_{4}\right)$ ta có
$$
\left(x_{1}, x_{2}, x_{3}, x_{4}\right)=\left(\frac{1}{3} a, \frac{2}{3} a, \frac{2}{3} a, a\right)
$$
với $a$ là một số nào đó. Kết hợp với điều kiện $x_{1}+x_{2}+x_{3}+x_{4}=200$, suy ra số muỗi tương ứng của các phòng $1,2,3,4$ ở trạng thái ổn định là $25 ; 50 ; 50 ; 75$.

Bài 4.
(a): Ký hiệu các viên gạch ở hàng thứ 2 lần lượt là $A, B, C, D, E$.
![](https://cdn.mathpix.com/cropped/2025_07_02_192ec19386869b40ea08g-06.jpg?height=312&width=1100&top_left_y=2248&top_left_x=484)

Nhận thấy một trong các viên gạch $A, B, C, D, E$ phải được chọn.
Với viên gạch $A$, có 3 cách chọn một viên gạch ở hàng 1 không kề với $A$. Tương tự, có 3 cách chọn một viên gạch ở hàng 3 không kề với $A$. Suy ra có $3 \times 3=9$ cách chọn ra ba viên gạch không kề nhau, một từ mỗi hàng, trong đó viên ở hàng 2 là $A$.
Với viên gạch $B$, có 3 cách chọn một viên gạch ở hàng 1 không kề với $B$. Tương tự, có 3 cách chọn một viên gạch ở hàng 3 không kề với $B$. Suy ra có $3 \times 3=9$ cách chọn ra ba viên gạch không kề nhau, một từ mỗi hàng, trong đó viên ở hàng 2 là $B$.
Với các tính toán tương tự,
- Có $3 \times 3=9$ cách chọn ba viên gạch không kề nhau, một từ mỗi hàng, trong đó viên ở hàng 2 là $C$.
- Có $3 \times 3=9$ cách chọn ba viên gạch không kề nhau, một từ mỗi hàng, trong đó viên ở hàng 2 là $D$.
- Có $4 \times 4=16$ cách chọn ba viên gạch không kề nhau, một từ mỗi hàng, trong đó viên ở hàng 2 là $E$.
Vì thế tổng số các cách chọn là
$$
9+9+9+9+16=52
$$
(b): Ký hiệu các viên gạch ở hàng 2 là $K, H, L, M, N$ và ở hàng 3 là $X, Y, Z, T, U$.
![](https://cdn.mathpix.com/cropped/2025_07_02_192ec19386869b40ea08g-07.jpg?height=418&width=1109&top_left_y=1656&top_left_x=482)
Để lấy ra các viên gạch ở hàng 2 và hàng 3, ta có các cách sau: $K Y, K Z, K T, K U$, $H Z, H T, H U, L X, L T, L U, M X, M Y, M U, N X, N Y, N Z$.
Gọi $k$ (tương ứng $h, l, m, n$ ) là số cách chọn ra một viên gạch ở hàng 1 không kề với $K$ (tương ứng $H, L, M, L$ ).
Tương tự, gọi $x$ (tương ứng $y, z, t, u$ ) là số cách chọn ra một viên gạch ở hàng 4 không kề với $X$ (tương ứng $Y, Z, T, U$ ).
Khi đó số cách chọn ra 4 viên gạch từ mỗi hàng, trong đó các viên ở hàng 2,3 tương ứng là $P, Q$, với $P \in\{K, H, L, M, N\}, Q \in\{X, Y, Z, T, U\}$ bằng pq. (Ví dụ, $P=K, Q=Y$, thì số cách chọn là ky.)
Dễ thấy,
$$
k=u=4, h=l=m=n=x=y=z=t=3 \text {. }
$$
Vì thế số các cách chọn ra 4 viên gạch thỏa mãn bài toán bằng
$$
\begin{aligned}
& k y+k z+k t+k u+h z+h t+h u+l x+l t+l u+m x+m y+m u+n x+n y+n z \\
= & 4 \cdot 3+4 \cdot 3+4 \cdot 3+4 \cdot 4+3 \cdot 3+3 \cdot 3+3 \cdot 4+3 \cdot 3+3 \cdot 3+3 \cdot 4+3 \cdot 3+ \\
& +3 \cdot 3+3 \cdot 4+3 \cdot 3+3 \cdot 3+3 \cdot 3 \\
= & 9 \cdot 3 \cdot 3+6 \cdot 4 \cdot 3+4 \cdot 4=81+72+16=169 .
\end{aligned}
$$

Bài 5.
(a): Dùng khai triển Laplace ta có
$$
\begin{aligned}
\operatorname{det}(A) & =-\left(x^{3}+y^{3}+z^{3}\right)+3 x y z \\
& =-(x+y+z)\left(x^{2}+y^{2}+z^{2}-x y-y z-z x\right)
\end{aligned}
$$
Như vậy $\operatorname{det}(A)=0$ khi và chỉ khi $x+y+z=0$ hoặc $x^{2}+y^{2}+z^{2}-x y-y z-z x=0$. Điều kiện sau tương đương $x=y=z$. Do đó không gian con cần tìm $V$ với số chiều 2 là tập nghiệm của phương trình $x+y+z=0$. Một cơ sở của nó là $((-1,1,0) ;(-1,0,1))$.
(b): Giả sử $x, y, z \in \mathbb{Z}$ thỏa mãn $A(x, y, z)=24$. Thế thì
$$
-(x+y+z)\left(x^{2}+y^{2}+z^{2}-x y-y z-z x\right)=24 .
$$
Do đó một trong hai số $x+y+z$ và $x^{2}+y^{2}+z^{2}-x y-y z-z x$ phải chia hết cho 3. Mặt khác
$$
x^{2}+y^{2}+z^{2}-x y-y z-z x=(x+y+z)^{2}-3(x y+y z+z x) .
$$
Thế thì $x+y+z$ và $x^{2}+y^{2}+z^{2}-x y-y z-z x$ cùng chia hết cho 3 . Lúc này tích của hai số sẽ chia hết cho 9 . Tuy nhiên 24 không chia hết cho 9 , nên điều này vô lý. Từ đó suy ra không tồn tại các số nguyên $x, y, z$ thỏa mãn đề bài.