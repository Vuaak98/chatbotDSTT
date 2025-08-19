Bài 5.1 (ĐH Tân Trào). 
Dễ thấy, $X$ có các giá trị riêng $\lambda_1=1$ và $\lambda_2=\lambda_3=2$. Với $\lambda_1=1$, có 1 véctơ riêng là $\alpha_1=(1 ;-5 ; 11)$. Với $\lambda_2=\lambda_3=2$, có một véctơ riêng, $\alpha_2=(0 ; 0 ; 1)$. Do đó, $X$ không chéo hóa được.
Vận dụng tính chéo hóa của một ma trận, ta chọn $Y$ và $D$ có dạng
$$
D=\left[\begin{array}{lll}
1 & 0 & 0 \\
0 & 2 & 0 \\
0 & 0 & c
\end{array}\right], Y=\left[\begin{array}{ccc}
1 & 0 & x \\
-5 & 0 & y \\
11 & 1 & z
\end{array}\right]
$$
Theo giả thiết, ta có $X Y=\left[\begin{array}{ccc}1 & 0 & x \\ -5 & 0 & 5 x+2 y \\ 11 & 1 & 4 x+3 y+2 z\end{array}\right], Y D=\left[\begin{array}{ccc}1 & 0 & x c \\ -5 & 0 & y c \\ 11 & 1 & z c\end{array}\right]$.
Suy ra
$$
\left\{\begin{array} { l } 
{ x + + = x c } \\
{ 5 x + 2 y + = y c } \\
{ 4 x + 3 y + 2 z = z c }
\end{array} \rightarrow \left\{\begin{array}{l}
c=1 \\
x=1 \\
y=5 \\
z=11
\end{array} \rightarrow D=\left[\begin{array}{lll}
1 & 0 & 0 \\
0 & 2 & 0 \\
0 & 0 & 1
\end{array}\right], Y=\left[\begin{array}{ccc}
1 & 0 & 1 \\
-5 & 0 & -5 \\
11 & 1 & 11
\end{array}\right]\right.\right.
$$
Thử lại $X Y=\left[\begin{array}{ccc}1 & 0 & 1 \\ -5 & 0 & -5 \\ 11 & 2 & 11\end{array}\right]=Y D$.

Bài 5.2 (ĐH Vinh). 
(a) Ta có
$$
\operatorname{det} A=\left|\begin{array}{ccc}
5-\lambda & 6 & -9 \\
1 & 4-\lambda & -3 \\
1 & 2 & -1-\lambda
\end{array}\right|=(\lambda-2)^2(4-\lambda)
$$
Vậy ma trận A có hai giá trị riêng $\lambda_1=2$ và $\lambda_2=4$.
- Ứng với giá trị riêng $\lambda_1=2$, gọi $X=\left(x_1, x_2, x_3\right) \neq(0,0,0)$ là vectơ riêng tương ứng. Khi đó, $A X=2 X$. Điều này trở thành:
$$
\left\{\begin{array}{cc}
3 x_1+6 x_2-9 x_3 & =0 \\
x_1+2 x_2-3 x_3 & =0 \\
x_1+2 x_2-3 x_3 & =0
\end{array}\right.
$$
Hệ tương đương với $x_1+2 x_2-3 x_3=0$. Từ đó suy ra tất cả các vectơ riêng của ma trận A ứng với giá trị riêng $\lambda_1=2$ là ( $-2 \alpha+3 \beta, \alpha, \beta$ ) với mọi $\alpha^2+\beta^2 \neq 0$.
- Ứng với giá trị riêng $\lambda_2=4$, gọi $X=\left(x_1, x_2, x_3\right) \neq(0,0,0)$ là vectơ riêng tương ứng. Khi đó, $A X=4 X$. Điều này trở thành:
$$
\begin{cases}x_1+6 x_2-9 x_3 & =0 \\ x_1-3 x_3 & =0 \\ x_1+2 x_2-5 x_3 & =0\end{cases}
$$
Giải hệ này ta thu được tất cả các vectơ riêng của ma trận A ứng với giá trị riêng $\lambda_2=4$ là $(3 \alpha, \alpha, \alpha)$ với mọi $\alpha \neq 0$.
(b) Với giá trị riêng $\lambda=2$, chọn 02 vectơ riêng độc lập tuyến tính $v_1=(-2,1,0)$ và $v_2=(3,0,1)$. Với giá trị riêng $\lambda=4$, chọn vectơ riêng $v_3=(3,1,1)$. Ma trận A chéo hóa được $A=P \cdot B \cdot P^{-1}$, trong đó
$$
B=\left(\begin{array}{ccc}
2 & 0 & 0 \\
0 & 2 & 0 \\
0 & 0 & 4
\end{array}\right) ; P=\left(\begin{array}{ccc}
-2 & 3 & 3 \\
1 & 0 & 1 \\
0 & 1 & 1
\end{array}\right) ; P^{-1}=\left(\begin{array}{ccc}
-1 / 2 & 0 & 3 / 2 \\
-1 / 2 & -1 & 5 / 2 \\
1 / 2 & 1 & -3 / 2
\end{array}\right) .
$$
Ta có
$$
\begin{aligned}
A^n & =\left(\begin{array}{ccc}
-2 & 3 & 3 \\
1 & 0 & 1 \\
0 & 1 & 1
\end{array}\right) \cdot\left(\begin{array}{ccc}
2^n & 0 & 0 \\
0 & 2^n & 0 \\
0 & 0 & 4^n
\end{array}\right) \cdot\left(\begin{array}{ccc}
-1 / 2 & 0 & 3 / 2 \\
-1 / 2 & -1 & 5 / 2 \\
1 / 2 & 1 & -3 / 2
\end{array}\right) \\
& =\left(\begin{array}{ccc}
6.4^{n-1}-2^{n-1} & 3\left(4^n-2^n\right) & 9\left(2^{n-1}-2.4^{n-1}\right) \\
2.4^{n-1}-2^{n-1} & 4^n & 3\left(2^{n-1}-2.4^{n-1}\right) \\
2.4^{n-1}-2^{n-1} & 4^n-2^n & 5.2^{n-1}-6.4^{n-1}
\end{array}\right) .
\end{aligned}
$$
Thay $n=2024$ ta thu được
$$
A^{2024}=\left(\begin{array}{ccc}
6.4^{2023}-2^{2023} & 3\left(4^{2024}-2^{2024}\right) & 9\left(2^{2023}-2.4^{2023}\right) \\
2.4^{2023}-2^{2023} & 4^{2024} & 3\left(2^{2023}-2.4^{2023}\right) \\
2.4^{2023}-2^{2023} & 4^{2024}-2^{2024} & 5.2^{2023}-6.4^{2023}
\end{array}\right) .
$$
(c) Sử dụng công thức khai triển Taylor: $e^x=\lim _{n \rightarrow+\infty} \sum_{k=0}^n \frac{1}{k!} x^k$ và
$$
A^k=\left(\begin{array}{ccc}
\frac{3.4^k-2^k}{2} & 3\left(4^k-2^k\right) & \frac{9\left(2^k-4^k\right)}{2} \\
\frac{4^k-2^k}{2} & 4^k & \frac{3\left(2^k-4^k\right)}{2} \\
\frac{4^k-2^k}{2} & 4^k-2^k & \frac{5.2^k-3.4^k}{2}
\end{array}\right),
$$
ta suy ra
$$
e^A=\left(\begin{array}{ccc}
\frac{3 \cdot e^4-e^2}{2} & 3\left(e^4-e^2\right) & \frac{9\left(e^2-e^4\right)}{2} \\
\frac{e^4-e^2}{2} & e^4 & \frac{3\left(e^2-e^4\right)}{2} \\
\frac{e^4-e^2}{2} & e^4-e^2 & \frac{5 \cdot e^2-3 \cdot e^4}{2}
\end{array}\right) .
$$

Bài 5.3 (ĐH Công nghệ Thông tin). 
(a) Ta kiểm tra 2 tính chất của $\varphi$ là:
$$
\begin{aligned}
\varphi(p(x)+q(x)) & =\varphi(p(x))+\varphi(q(x)) \\
\varphi(k p(x)) & =k \varphi(p(x))
\end{aligned}
$$
trong đó $p(x)=a_0+a_1 x+a_2 x^2, q(x)=b_0+b_1 x+b_2 x^2$ và $k \in \mathbb{R}$. Ma trận của $\varphi$ đối với cơ sở $\left\{1, x, x^2\right\}$ là
$$
A=\left[\begin{array}{ccc}
7 & -12 & -2 \\
3 & -4 & 0 \\
-2 & 0 & -2
\end{array}\right]
$$
(b) Đa thức đặc trưng của $A: P_A(\lambda)=-\lambda(\lambda+1)(\lambda-2)$. Các trị riêng của $A$ là $0,-1,2$ đều là các trị riêng đơn (bội 1 ) nên $A$ chéo hóa được.
- Các véc tơ riêng của $A$ tương ứng với $\lambda_1=0$ là $[4 a 3 a-4 a]^T$ với $a \neq 0$.
- Các véc tơ riêng của $A$ tương ứng với $\lambda_2=-1$ là $[a a-2 a]^T$ với $a \neq 0$.
- Các véc tơ riêng của $A$ tương ứng với $\lambda_3=2$ là $[2 a a-a]^T$ với $a \neq 0$
Ma trận $T=\left[\begin{array}{ccc}4 & 1 & 2 \\ 3 & 1 & 1 \\ -4 & -2 & -1\end{array}\right]$ và $T^{-1}=\left[\begin{array}{ccc}-1 & 3 & 1 \\ 1 & -4 & -2 \\ 2 & -4 & -1\end{array}\right]$ và $T^{-1} A T=\left[\begin{array}{ccc}0 & 0 & 0 \\ 0 & -1 & 0 \\ 0 & 0 & 2\end{array}\right]$
(c) Với $p(x)=-1-2 x+3 x^2$ và tọa độ của $p(x)$ đối với cơ sở $B=\left\{1, x, x^2\right\}$ là $\left[\begin{array}{c}-1 \\ -2 \\ 3\end{array}\right]$. Khi đó
$$
\left[\varphi^{2024}(p(x))\right]_B=A^{2024}\left[\begin{array}{c}
-1 \\
-2 \\
3
\end{array}\right]=\left[\begin{array}{c}
1+6.2^{2024} \\
1+3.2^{2024} \\
-2-3.2^{2024}
\end{array}\right]
$$
Như vậy $\varphi^{2024}(p(x))=\left(1+6.2^{2024}\right)+\left(1+3.2^{2024}\right) x+\left(-2-3.2^{2024}\right) x^2$.

Bài 5.4 (ĐH Ngoại Thương). 
(a) Các giá trị riêng của $A$ là $1 ;-2 ; 4$, tìm được qua đa thức đặc trưng. 
(b) Gọi ba véctơ riêng ứng với ba giá trị riêng $1 ;-2 ; 4$ là $a, b, c$. Ta có
$$
\begin{aligned}
& B a=\left(20.1^5-2.1^2+4\right) a=22 a, \\
& B b=\left(20 .(-2)^5-2 .(-2)^2+4\right) b=-644 b, \\
& B c=\left(20.4^5-2.4^2+4\right) c=20452 c .
\end{aligned}
$$
Do đó các giá trị riêng của $B$ là $22,-644,20452$.

Bài 5.5 (ĐH Trà Vinh). 
Đa thức đặc trưng của $A$ là $x(x+1)(x-2)$ có ba nghiệm phân biệt nên $A$ chéo hóa được. Các giá trị riêng là $0,-1,2$ và các véctơ riêng tương ứng là $(4,3,-4)^T,(1,1,-2)^T,(2,1,-1)^T$. Do đó
$$
P=\left(\begin{array}{ccc}
4 & 1 & 2 \\
3 & 1 & 1 \\
-4 & -2 & -1
\end{array}\right), P^{-1} A P=\left(\begin{array}{ccc}
0 & 0 & 0 \\
0 & -1 & 0 \\
0 & 0 & 2
\end{array}\right)
$$
Suy ra
$$
A^{2024}=P\left(\begin{array}{ccc}
0 & 0 & 0 \\
0 & -1 & 0 \\
0 & 0 & 2
\end{array}\right)^{2024} P^{-1}=\left(\begin{array}{ccc}
1+2^{2026} & -4-2^{2027} & -2-2^{2025} \\
1+2^{2025} & -4-2^{2026} & -2-2^{2024} \\
-2-2^{2025} & 8+2^{2026} & 4+2^{2024}
\end{array}\right)
$$