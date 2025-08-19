Bài 1.
(a) Với $a=-1$ thì ma trận $A$ bằng
$$
A=\left(\begin{array}{llll}
1 & 0 & 1 & 0 \\
2 & 1 & 0 & 1 \\
1 & 0 & 1 & 0 \\
0 & 1 & 2 & 1
\end{array}\right)
$$
Hạng của ma trận lúc này bằng 3 .
(b) Dùng biến đổi sơ cấp hàng và khai triển Laplace ta có
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
& =2(a+3)-2(a+2)(a+3)-(a+3)(2 a+2) \\
& =-4(a+1)(a+3)
\end{aligned}
$$
Do đó định thức $\operatorname{det}(A)>0$ khi và chỉ khi $-3<a<-1$.
(c) Nếu $a \neq-3,-1$, thì $\operatorname{det}(A) \neq 0$. Do đó trong trường hợp này phương trình chỉ có nghiệm tầm thường, số chiều của không gian nghiệm tương ứng bằng 0.
Với $a \in\{-1,-3\}$, tính cụ thể được $\operatorname{rank}(A)=3$. Số chiều của không gian nghiệm tương ứng bằng $4-\operatorname{rank}(A)=1$.

Bài 2.
(a) Gọi $a_{i}$ là số muỗi ban đầu tương ứng của phòng $i \in\{1,2,3,4\}$. Từ giả thiết ta có hệ phương trình:
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
(b) Gọi $x_{1}, x_{2}, x_{3}, x_{4}$ là số muỗi tương ứng của các phòng $1,2,3,4$ ở trạng thái ổn định. Khi đó $x_{1}+x_{2}+x_{3}+x_{4}=200$, và sau một phút số muỗi mỗi phòng tương ứng sẽ là $x_{1}^{\prime}, x_{2}^{\prime}, x_{3}^{\prime}, x_{4}^{\prime}$ trong đó
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

Bài 3.
(a) Thay $x=1$ vào giả thiết ta có $0 \cdot P(1)=3 \cdot P(1)$. Do đó $P(1)=0$. Lại thay $x=0$ ta có $2 \cdot P(0)=(-1) \cdot P(1)$. Kết hợp với $P(1)=0$, suy ra $P(0)=0$. Lại thay $x=-1$ và kết hợp với $P(0)=0$, suy ra $P(-1)=0$. Do đó đa thức $P(x)$ có ít nhất ba nghiệm thực là $1,0,-1$.
(b): Từ phần (a) suy ra $P(x)=x(x-1)(x+1) G(x)$, với $G(x)$ là một đa thức nào đó với hệ số thực. Thay vào đẳng thức ban đầu ta được:
$$
x(x-1)(x+1)(x+2) G(x+1)=(x+2) x(x-1)(x+1) G(x)
$$
Từ đó suy ra $G(x)=G(x+1)$ với mọi $x \notin\{0, \pm 1,-2\}$. Do đó $G(x)=c$ là một đa thức hằng số. Từ đó suy ra
$$
P(x)=c x(x-1)(x+1)
$$
với $c$ là một số thực bất kỳ. Thử lại suy ra tất cả các đa thức thỏa mãn đề bài là $P(x)=c x(x-1)(x+1)$ với $c \in \mathbb{R}$.

Bài 4.
(a) Dùng khai triển Laplace ta có
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
x^{2}+y^{2}+z^{2}-x y-y z-z x=(x+y+z)^{2}-3(x y+y z+z x)
$$
Thế thì $x+y+z$ và $x^{2}+y^{2}+z^{2}-x y-y z-z x$ cùng chia hết cho 3 . Lúc này tích của hai số sẽ chia hết cho 9 . Tuy nhiên 24 không chia hết cho 9 , nên điều này vô lý. Từ đó suy ra không tồn tại các số nguyên $x, y, z$ thỏa mãn đề bài.

Bài 5.
(a) Từ giả thiết $A B-B A=B^{2} A$, ta có
$$
A^{-1}\left(B^{2}+B\right) A=A^{-1} B^{2} A+A^{-1} B A=A^{-1}(A B-B A)+A^{-1} B A=A^{-1} A B=B
$$
Do đó $B=A^{-1}\left(B^{2}+B\right) A$.
(b) Ví dụ về một cặp ma trận tốt là
$$
A_{2}=\left(\begin{array}{ll}
0 & 1 \\
1 & 0
\end{array}\right), B_{2}=\left(\begin{array}{cc}
-1 & 1 \\
-1 & -1
\end{array}\right)
$$
(c) Ta chỉ ra tồn tại cặp hai ma trận $(A, B)$ là tốt khi và chỉ khi $n$ là một số chẵn. Đầu tiên giả sử tồn tại hai ma trận $A, B$ có cùng cấp $n$ thỏa mãn đề bài với $n$ là một số lẻ. Theo phần (a), $B$ và $B^{2}+B$ đồng dạng, suy ra chúng có cùng tập các giá trị riêng. Vì cấp của $B$ lẻ, nên đa thức đặc trưng của $B$ là đa thức bậc lẻ với hệ số thực, suy ra $B$ có ít nhất một giá trị riêng thực $\lambda_{1}$. Do đó $B^{2}+B$ có giá trị riêng thực $\lambda_{2}=\lambda_{1}^{2}+\lambda_{1}$. Thật vậy
$$
\left|\left(B^{2}+B\right)-\left(\lambda_{1}^{2}+\lambda_{1}\right) I_{n}\right|=\left|\left(B-\lambda I_{n}\right)\right| \cdot\left|\left(B+\lambda I_{n}\right)+I_{n}\right|=0
$$
Theo điều trên $B$ và $B^{2}+B$ có cùng tập giá trị riêng, nên $B$ cũng nhận $\lambda_{2}=$ $\lambda_{1}^{2}+\lambda_{1}$ là một giá trị riêng thực. Lặp lại lập luận trên, $B$ cũng nhận $\lambda_{3}=$ $\lambda_{2}^{2}+\lambda_{2}, \lambda_{4}=\lambda_{3}^{2}+\lambda_{3}, \ldots$ làm các giá trị riêng. Vì tập giá trị riêng của một ma trận chỉ là hữu hạn, nên dãy $\left\{\lambda_{1}, \lambda_{2}, \ldots\right\}$ tuần hoàn, nghĩa là tồn tại $k \neq l \in \mathbb{Z}^{+}$ sao cho
$$
\left\{\begin{array}{l}
\lambda_{k+1}=\lambda_{k}^{2}+\lambda_{k} \\
\lambda_{k+2}=\lambda_{k+1}^{2}+\lambda_{k+1} \\
\cdots \\
\lambda_{l}=\lambda_{l-1}^{2}+\lambda_{l-1} \\
\lambda_{k}=\lambda_{l}^{2}+\lambda_{l}
\end{array}\right.
$$
Thế thì $\lambda_{k}^{2}+\cdots+\lambda_{l}^{2}=0$, với $\lambda_{k}, \ldots, \lambda_{l} \in \mathbb{R}$. Do đó
$$
\lambda_{k}=\ldots=\lambda_{l}=0
$$
Từ đó suy ra $B$ nhận $\lambda=0$ là một giá trị riêng, suy ra $B$ không khả nghịch, suy ra vô lý. Vậy cặp ma trận cùng cấp lẻ không thể là tốt.
Bây giờ ta chứng minh với mọi $n$ chẵn, luôn tồn tại $A, B$ cấp $n$ thỏa mãn đề bài. Như phần (b), với $n=2$ ta đã chọn được cặp ma trận tốt
$$
A_{2}=\left(\begin{array}{ll}
0 & 1 \\
1 & 0
\end{array}\right), B_{2}=\left(\begin{array}{cc}
-1 & 1 \\
-1 & -1
\end{array}\right)
$$
Với $n=2 k$ là một số chẵn bất kỳ, ta chọn ma trận khối:
$$
\begin{aligned}
& A=A_{2} \oplus \cdots \oplus A_{2}, \\
& B=B_{2} \oplus \cdots \oplus B_{2},
\end{aligned}
$$
với số khối bằng $k$. Khi đó cặp $(A, B)$ là tốt với cấp của $A, B$ bằng $n$. Vậy tập các số $n$ thỏa mãn đề bài là $n$ chẵn.