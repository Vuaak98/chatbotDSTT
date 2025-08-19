Bài 1. 
(a)
$$
A^2=\left(\begin{array}{ccc}
-4 & -4 & 4 \\
-8 & -8 & 8 \\
-16 & -16 & 16
\end{array}\right), \quad A^4=\left(\begin{array}{ccc}
-16 & -16 & 16 \\
-32 & -32 & 32 \\
-64 & -64 & 64
\end{array}\right)
$$
(b)
Cách 1: Tính trực tiếp.
- Tính $\operatorname{rank}(A)=2$.
- Tính
$$
A^2=\left(\begin{array}{ccc}
-4 & -4 & 4 \\
-8 & -8 & 8 \\
-16 & -16 & 16
\end{array}\right)
$$
và do đó $\operatorname{rank}\left(A^2\right)=1$.
- Tổng quát, với $k>1$ thì
$$
A^k=\left(\begin{array}{ccc}
-(-2)^k & -(-2)^k & (-2)^k \\
(-2)^{k+1} & (-2)^{k+1} & -(-2)^{k+1} \\
-(-2)^{k+2} & -(-2)^{k+2} & (-2)^{k+2}
\end{array}\right)=(-2)^k\left(\begin{array}{ccc}
-1 & -1 & 1 \\
-2 & -2 & 2 \\
-4 & -4 & 4
\end{array}\right) .
$$
và $\operatorname{rank}\left(A^k\right)=1$.
Vậy $N=2$.
Cách 2: Sử dụng dạng chuẩn Jordan.
- Tính dạng chuẩn Jordan của $A$, có
$$
A \sim B=\left(\begin{array}{ccc}
0 & 1 & 0 \\
0 & 0 & 0 \\
0 & 0 & -2
\end{array}\right)
$$
- Do đó
$$
A^k \sim B^k=\left(\begin{array}{ccc}
0 & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & (-2)^k
\end{array}\right)
$$
với mọi $k>1$. Nói riêng, $\operatorname{ran} k\left(A^k\right)=1$ với mọi $k>1$.
Vậy số nhỏ nhất cần tìm là $N=2$.

Bài 2. 
(a)
Cách 1:
- Gọi $x_k, y_k$ tương ứng là số dân tại các vùng nông thôn và vùng đô thị sau $k$ nằm. Ví dụ, $x_0=x, y_0=y$. Ta có $x_{k+1}=\frac{1}{2} x_k+\frac{1}{4} y_k, y_{k+1}=\frac{3}{4} y_k+\frac{1}{2} x_k$. Nói cách khác
$$
\left[\begin{array}{l}
x_{k+1} \\
y_{k+1}
\end{array}\right]=\left[\begin{array}{cc}
\frac{1}{2} & \frac{1}{4} \\
\frac{1}{2} & \frac{3}{4}
\end{array}\right] \cdot\left[\begin{array}{l}
x_k \\
y_k
\end{array}\right]
$$
- Từ đó suy ra,
$$
\left[\begin{array}{l}
x_k \\
y_k
\end{array}\right]=A^n \cdot\left[\begin{array}{l}
x_0 \\
y_0
\end{array}\right]
$$
trong đó $A=\left[\begin{array}{ll}\frac{1}{2} & \frac{1}{4} \\ \frac{1}{2} & \frac{3}{4}\end{array}\right]$.
- Đa thức đặc trưng của $A$ là $x^2-\frac{5}{4} x+\frac{1}{4}=(x-1)\left(x-\frac{1}{4}\right)$. Từ đây, ta suy ra $A$ có các véctơ riêng $\left[\begin{array}{l}1 \\ 2\end{array}\right],\left[\begin{array}{c}1 \\ -1\end{array}\right]$ tương ứng với các giá trị riêng $1,1 / 4$. Vậy, nếu ta đặt $P=\left[\begin{array}{cc}1 & 1 \\ 2 & -1\end{array}\right]$, thì $P^{-1} A P=D$, trong đó $D$ là ma trận đường chéo với các hệ số trên đường chéo lần lượt là 1 và $1 / 4$. Ta dễ dàng tính được $P^{-1}=\left[\begin{array}{cc}\frac{1}{3} & \frac{1}{3} \\ \frac{2}{3} & -\frac{1}{3}\end{array}\right]$.
- Suy ra $A=P D P^{-1}$ và
$$
A^k=P D^k P^{-1}=\left[\begin{array}{cc}
1 & 1 \\
2 & -1
\end{array}\right]\left[\begin{array}{cc}
1 & 0 \\
0 & \frac{1}{4^k}
\end{array}\right]\left[\begin{array}{cc}
\frac{1}{3} & \frac{1}{3} \\
\frac{2}{3} & -\frac{1}{3}
\end{array}\right]=\left[\begin{array}{cc}
\frac{1}{3}+\frac{2}{34^k} & \frac{1}{3}-\frac{1}{34^k} \\
\frac{2}{3}-\frac{2}{34^k} & \frac{2}{3}+\frac{1}{34^k}
\end{array}\right] .
$$
- Từ đó,
$$
\begin{aligned}
& x_k=\left(\frac{1}{3}+\frac{2}{3 \cdot 4^k}\right) x+\left(\frac{1}{3}-\frac{1}{3 \cdot 4^k}\right) y \\
& y_k=\left(\frac{2}{3}-\frac{2}{3 \cdot 4^k}\right) x+\left(\frac{2}{3}+\frac{1}{3 \cdot 4^k}\right) y
\end{aligned}
$$

Lưu ý: Để tính $A^k$ cũng có thể dùng quy nạp theo $n$.
Cách 2: Lập luận tương tự trên, ta có $x_{k+1}=\frac{1}{2} x_k+\frac{1}{4} y_k, y_{k+1}=\frac{3}{4} y_k+\frac{1}{2} x_k$. Thay $y_k=4 x_{k+1}-2 x_k$ vào phương trình thứ hai, ta được
$$
4 x_k-5 x_{k-1}+x_{k-2}=0
$$
Từ đó dẫn đến $x_k-x_{k-1}=\frac{1}{4^k} y-2 \frac{1}{4^k} x$. Vậy
$$
x_k=x_0+\sum_{i=1}^k \frac{1}{4^i} y-2 \sum_{i=1}^k \frac{1}{4^i} x
$$

Từ đó suy ra
$$
x_k=\left(\frac{1}{3}+\frac{2}{3 \cdot 4^k}\right) x+\left(\frac{1}{3}-\frac{1}{3 \cdot 4^k}\right) y,
$$

Tương tự
$$
y_k=\left(\frac{2}{3}-\frac{2}{3 \cdot 4^k}\right) x+\left(\frac{2}{3}+\frac{1}{3 \cdot 4^k}\right) y .
$$
(b) Câu trả lời là không. Nếu $y_k=4 x_k$ thì thay vào phương trình trên ta được
$$
\left(2+10 / 4^k\right) x+\left(2-5 / 4^k\right) y=0 .
$$

Vỉ $x, y>0$ nên điều này chỉ có thể xảy ra $k=0$ và $y=4 x$, trái với giả thiết.

Bài 3. 
(a) Ta có $X A=X^3=A X$.
(b) Gọi ma trận bên phải là $A$, như vậy $X^2=A$. Dưới đây là hai cách giải

Cách 1: Giải hai hệ $A X=X A$ và $X^2=A$.
- Giả sử $X=\left(x_{i j}\right)_{3 \times 3}$. Từ $A X=X A$, ta được hệ phương trình của $x_{i j}$, rút gọn lại là
$$
\left\{\begin{array}{l}
x_{21}=x_{31}=x_{32}=x_{12}=0, \\
x_{22}+6 x_{23}-x_{33}=0 \\
x_{11}+15 x_{13}-x_{33}=0 .
\end{array}\right.
$$
- Kết hợp với $X^2=A$, ta được $x_{11}^2=1, x_{22}^2=4, x_{33}^2=16$. Từ đó tính được $x_{13}, x_{23}$, các giá trị nhận được đều thỏa mãn $X^2=A$. Vậy có tất cả $2^3=8 \mathrm{ma}$ trận thỏa mãn đề bài.

Cách 2: - Đa thức đặc trưng của $A$ là $\Pi_A(x)=\operatorname{det}\left(x I_3-A\right)=(x-1)(x-$ 4) $(x-16)$.
- Đa thức có 3 nghiệm đơn nên $A$ có thể chéo hoá được với các hệ số trên đường chéo bằng $1,4,16$. Như vậy, ta có thể viết $A=P^{-1} D P$, trong đó $D$ là ma trận vuông với các hệ số trên đường chéo lần lượt là $1,4,16$ và $P$ là một ma trận khả nghịch. Ta suy ra $P X^2 P^{-1}=D$.
- Như vậy, nếu ta đặt $P X P^{-1}=Y$ thì phương trình ban đầu trở thành
$$
Y^2=D . \quad(*)
$$

Theo câu (a), ta suy ra $Y D=D Y$. Từ đây, dễ thấy $Y$ phải là một ma trận đường chéo. Gọi $y_1, y_2, y_3$ tương ứng là các hệ số trên đường chéo của $Y$. Thế thì (*) tương đương với $y_1^2=1, y_2^2=4, y_3^2=16$. Từ đây, ta suy ra 8 nghiệm là $\left(y_1, y_2, y_3\right)=( \pm 1, \pm 2, \pm 4)$. Ta kết luận rằng ( ${ }^*$ ) có 8 nghiệm và vì thế phương trình ban đầu có 8 nghiệm.

Bài 4. 
(a) Đặt $A=\left(\begin{array}{ll}a & b \\ c & d\end{array}\right)$ với $a, b, c, d>0$. Đa thức đặc trưng của $A$ có dạng $x^2-(a+d) x+(a d-b c)$. Biệt thức của đa thức này $\Delta=(a-d)^2+4 b c>0$. Vậy $A$ có 2 giá trị riêng phân biệt và đều là số thực.
Vì tổng hai nghiệm bằng $a+d>0$ nên trị riêng có giá trị tuyệt đối lớn nhất phải là số dương.
(b) Gọi $t$ là trị riêng lớn nhất và $v=(x, y)$ là véc tơ riêng ứng với $t$. Ta có
$$
(a-t) x+b y=c x+(d-t) y=0
$$
Nếu $x$ và $y$ không cùng đấu thì $a-t$ và $b$ cùng đấu, $d-t$ và $c$ cùng đấu. Do đó $a-t$ và $d-t$ đều $>0$. Hay $t<\frac{1}{2}(a+d)$. Điều này mâu thuẫn với việc $t$ là giá trị riêng lớn nhất (vì tổng các trị riêng bằng $a+d$ ).
(c) $A$ có ít nhất một giá trị riêng khác 0 . Thật vậy, nếu tất cả các trị riêng của $A$ đều bằng 0 thì theo định lý Cayley-Hamilton, $A^3=0$. Điều này mâu thuẫn với việc $A$ là ma trận dương.
Đặt $t$ là trị riêng của $A$ mà có mô đun lớn nhất ( $t$ có thể là số phức). Sau đây ta ký hiệu $|x|$ là véc tơ mà thành phần là mô đun của các thành phần của véc tơ $x$. Ta viết $x \geq y$ nếu các tọa độ của $x$ đều $\geq$ tọa độ tương ứng của $y$. Giả sử $x$ là véc tơ riêng của $A$ ứng với $t$. Ta có (theo bất đẳng thức tam giác $|a+b| \leq|a|+|b|)$,
$$
|A x| \leq A|x|
$$
Từ đó
$$
|t||x|=|t x|=\leq A|x| .
$$
Ta cần chứng minh đấu bằng xảy ra. Giả sử trái lại. Đặt $B=A /|t|$. Thì $B|x|-|x|=y>0$. Nghĩa là véc tơ $y$ khác 0 và có các thành phần không âm. Từ đó $B y$ có tất cả các thành phần $>0$. Đặt $z:=B|x|$ thì ta có
$$
B z-z=B y .
$$
Từ tính chất của $B y$ nói trên, tồn tại $\lambda>1$ sao cho
$$
B z>\lambda z .
$$
Theo trên thì $z$ là véc tơ có các thành phần đều dương, $B$ có các trị riêng đều có mô đun $\leq 1$. Tác động $B$ nhiều lần vào bất đẳng thức cuối cùng ta suy ra vô lý.

Bài 5. 
(a) Kí hiệu các điểm được đánh dấu, theo chiều kim đồng hồ, lần lượt là $A_1, A_2, \ldots, A_6$. Dễ thấy rằng $A_1$ phải được nối với $A_2, A_6$ hoặc $A_4$.
- Nếu $A_1$ nối với $A_4$ thì ta phải nối $A_2$ với $A_3$ và $A_5$ với $A_6$.
- Nếu $A_1$ nối với $A_2$ thì hoặc là $A_6$ nối với $A_5$ còn $A_3$ nối với $A_4$, hoặc là $A_6$ nối với $A_3$ và $A_5$ nối với $A_4$.
- Tương tự, nếu $A_1$ nối với $A_6$ thì hoặc là $A_2$ nối với $A_3$ và $A_4$ với $A_5$ hoặc là $A_2$ nối với $A_5$ và $A_3$ với $A_4$.
Như vậy, có cả thảy 5 cách nối.
(b) Gọi $X$ là tập 3 điểm được gán các số $1,2,3$ và $Y$ là tập 3 điểm còn lại. Ta sẽ chỉ ra rằng tồn tại 3 dây cung không có điểm chung, mỗi dây cung nối một điểm của $X$ và một điểm của $Y$. Một cách nối như vậy thoả mãn yêu cầu bài toán vì tổng các số tương ứng với 3 dây cung này bằng $4+5+6-1-2-3=9$. 
- Dễ thấy rằng có một điểm của $X$ nằm kề một điểm của $Y$ (đó là hai điểm liên tiếp nếu ta đi theo chiều kim đồng hồ). Kẻ dây cung nối 2 điểm này rồi loại bỏ 2 điểm đánh dấu này lẫn dây cung đi, ta còn lại 4 điểm được đánh dấu trên đường tròn và 2 tập con $X^{\prime}, Y^{\prime}$ tương ứng, mỗi tập gồm 2 điểm được đánh dấu.
- Bây giờ, lập luận tương tự, ta cũng suy ra có một điểm của $X^{\prime}$ kề nhau với một điểm $Y^{\prime}$ trên đường tròn đã bỏ đi 2 điểm trước đó. Kẻ dây cung nối 2 điểm này cũng như dây cung nối 2 điểm còn lại. Bây giờ, khôi phục lại dây cung ban đầu. Dễ thấy, 3 dây cung được kẻ đôi một không có điểm chung. Bài toán được giải quyết.