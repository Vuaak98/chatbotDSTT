Bài 6.1 (ĐH Giao thông Vận tải). 
Ký hiệu $U$ là không gian tuyến tính bao gồm tất cả các đa thức có hệ số thực và có bậc không vượt quá 2024. Ký hiệu $V$ là không gian tuyến tính bao gồm tất cả các đa thức có hệ số thực và có bậc không vượt quá 2022. Với mỗi đa thức $Q(x)$ với hệ số thực, ta đặt
$$
\Phi[Q(x)]=Q(x+1)+Q(x-1)-2 Q(x)+7 Q \prime(x)
$$
Nếu $Q(x)=a x+b$ là đa thức có bậc không vượt quá 1 thì tính toán trực tiếp ta thu được $\Phi[Q(x)]=0$. Nếu $Q(x)$ là một đa thức bậc $n$ nào đấy với $n \geqslant 2$ và có số hạng dẫn là $a_{n} x^{n}$ thì $\Phi[Q(x)]$ là một đa thức có số hạng dẫn là $8 n(n-1) a_{n} x^{n-2}$ nên $\Phi[Q(x)] \neq 0$ và có bậc là $n-2$. Từ đây ta suy ra rằng, tương ứng $Q(x) \mapsto \Phi[Q(x)]$ xác định một ánh xạ $\Phi: U \rightarrow V$ từ không gian tuyến tính $U$ đến không gian tuyến tính $V$. Dễ dàng chỉ ra được $\Phi$ là một ánh xạ tuyến tính và theo phân tích trên
$$
\operatorname{Ker} \Phi=\{a x+b \mid a, b \in \mathbb{R}\}
$$
Ta nhận được $\operatorname{dim}(\operatorname{Ker} \Phi)=2$. Sử dụng $\operatorname{dim}(\operatorname{Im} \Phi)=\operatorname{dim} U-\operatorname{dim}(\operatorname{Ker} \Phi)=$ $2025-2=2023=\operatorname{dim} V$ ta suy ra được $\operatorname{Im} \Phi=V$ và $\Phi$ là một toàn cấu. Vậy với đa thức $P(x)$ cho trước có bậc 2022 là phần tử của $V$, luôn tồn tại đa thức $Q_{0}(x)$ có bậc 2024 (là phần tử của $U$ ) sao cho $\Phi\left[Q_{0}(x)\right]=P(x)$. Nếu $Q(x)$ là một đa thức nào đấy mà $\Phi[Q(x)]=P(x)$ thì $Q(x)$ cũng phải có bậc là 2024 và $Q(x) \in U$. Khi đó, $\Phi\left[Q-Q_{0}\right]=P-P=0$ nên $Q-Q_{0} \in \operatorname{Ker} \Phi$. Như vậy, tập hợp các đa thức $\mathrm{Q}(\mathrm{x})$ thỏa mãn yêu cầu $\Phi[Q(x)]=P(x)$ là các đa thức có dạng
$$
\begin{equation*}
Q(x)=Q_{0}(x)+a x+b, \quad a, b \in \mathbb{R} \tag{1}
\end{equation*}
$$
Đa thức hệ số thực $Q(x)$ nhận số phức $x=2+\sqrt{7} i$ là một nghiệm thì nó cũng nhận $x=2-\sqrt{7} i$ là một nghiệm. Điều này tương đương với $Q(x)$ phải chia hết cho đa thức bậc 2
$$
T(x)=(x-2-\sqrt{7} i)(x-2+\sqrt{7} i)=x^{2}-4 x+11 .
$$
Dễ dàng chỉ ra được trong tập hợp (1) ở trên chỉ có duy nhất một cặp hệ số thực $a, b$ để $Q(x)$ là bội của đa thức bậc hai $T(x)=x^{2}-4 x+11$. Như vậy, ta đã chỉ ra được điều phải chứng minh.

Bài 6.2 (ĐH Vinh). 
Ta có
$$
\begin{equation*}
P(x) \cdot P\left(2024 x^{4}\right)=P\left(x^{2024}+8 x^{4}\right) \text { với mọi } x \in \mathbb{R} \text {. } \tag{1}
\end{equation*}
$$
- Đầu tiên, ta xét trường hợp $P(x)$ là đa thức hằng. Thay $P(x)=c$ ta suy ra $c=0$ hoặc $c=1$.
- Tiếp theo, ta xét trường hợp $\operatorname{deg}(P(x)) \geq 1$. Thay $x=0$, ta suy ra rằng $P^{2}(0)=P(0)$. Điều này dẫn tới $P(0)=0$ hoặc $P(0)=1$.
Nếu $P(0)=0$ thì $P(x)=x^{s} Q(x)$ với $s \geq 1$ và $Q(0) \neq 0$. Thay vào (1) ta có
$$
x^{s} Q(x) 2024^{s} x^{4 s} Q\left(2024 x^{4}\right)=\left(x^{2024}+8 x^{4}\right)^{s} Q\left(x^{2024}+8 x^{4}\right) \text { với mọi } x \in \mathbb{R} .
$$
Điều này tương đương với
$$
x^{s} Q(x) 2024^{s} Q\left(2024 x^{4}\right)=\left(x^{2020}+8\right)^{s} Q\left(x^{2024}+8 x^{4}\right) \text { với mọi } x \in \mathbb{R} \text {. }
$$
Thay $x=0$ ta có $Q(0)=0$ : mâu thuẫn với $Q(0) \neq 0$.
Vậy
$$
\begin{equation*}
P(0)=1 \tag{2}
\end{equation*}
$$
Đạo hàm 2 vế (1) ta được
$$
\begin{equation*}
P^{\prime}(x) \cdot P\left(2024 x^{4}\right)+P(x) \cdot 8096 x^{3} \cdot P^{\prime}\left(2024 x^{4}\right)=\left(2024 x^{2023}+32 x^{3}\right) \cdot P^{\prime}\left(x^{2024}+8 x^{4}\right) \tag{3}
\end{equation*}
$$
Thay $x=0$ vào đẳng thức trên ta có $P^{\prime}(0) \cdot P(0)=0$. Suy ra $P^{\prime}(0)=0$ (do (2)). Do đó $P^{\prime}(x)=x^{r} . H(x)$ với $r \geq 1$ và $H(0) \neq 0$. Thay vào (3) ta có
$$
\begin{aligned}
x^{r} \cdot H(x) P\left(2024 x^{4}\right) & +P(x) \cdot 8096 x^{3} \cdot 2024^{r} x^{4 r} \cdot H\left(2024 x^{4}\right) \\
& =\left(2024 x^{2023}+32 x^{3}\right) \cdot\left(x^{2024}+8 x^{4}\right)^{r} \cdot P^{\prime}\left(x^{2024}+8 x^{4}\right)
\end{aligned}
$$
với mọi $x \in \mathbb{R}$. Điều này tương đương với
$$
\begin{aligned}
H(x) P\left(2024 x^4\right) & +P(x) \cdot 8096 x^3 \cdot 2024^r x^{3 r} \cdot H\left(2024 x^4\right) \\
& =\left(2024 x^{2023}+32 x^3\right) \cdot\left(x^{2023}+8 x^3\right)^r \cdot H\left(x^{2024}+8 x^4\right)
\end{aligned}
$$
với mọi $x \in \mathbb{R}$. Thay $x=0$ vào đẳng thức trên ta có $H(0) \cdot P(0)=0$. Điều này mâu thuẫn với $H(0) \neq 0$ và $P(0)=1$. Do vậy, không tồn tại đa thức $P(x)$ bậc lớn hơn 0 thỏa mãn yêu cầu bài toán.
Vậy, tất cả đa thức cần tìm là các đa thức hằng $P(x)=0$ và $P(x)=1$.

Bài 6.3 (ĐH Vinh). 
Nếu đa thức $P(x)$ bậc $m$ thì $P^{(k)}(x)=0$ với mọi $x \in \mathbb{R}$ và với mọi $k \geq m+1$. Suy ra $f(x)$ là tổng hữu hạn các đa thức, do đó $f(x)$ là một đa thức.
Theo công thức khai triển Taylor ta có
$$
\begin{aligned}
& P(x+1)=P(x)+P^{\prime}(x)+\frac{P^{\prime \prime}(x)}{2!}+\ldots \\
& P(x-1)=P(x)-P^{\prime}(x)+\frac{P^{\prime \prime}(x)}{2!}-\ldots
\end{aligned}
$$

Cộng vế theo vế hai đẳng thức trên ta suy ra
$$
\frac{1}{2}(P(x+1)+P(x-1))=P(x)+\frac{P^{\prime \prime}(x)}{2!}+\frac{P^{(4)}(x)}{4!}+\ldots=f(x)
$$

Vì $P(x)$ không có nghiệm thực nên nó giữ nguyên dấu trên $\mathbb{R}$. Điều này dẫn tới $P(x+1)$ và $P(x-1)$ cùng dương hoặc cùng âm với mọi $x \in \mathbb{R}$. Do đó, $f(x)>0$ luôn dương, hoặc luôn âm trên $\mathbb{R}$.
Từ đó, ta có điều phải chứng minh.

Bài 6.4 (ĐH Công nghệ Thông tin).
(a). Đa thức đặc trưng của $A$ là $p_{A}(\lambda)=-(\lambda-2)^{3}$. Vì $p_{A}(A)=0$ và $p(x)$ là đa thức có bậc nhỏ nhất thỏa mãn $p(A)=0$ nên $p(x)$ là ước của đa thức đặc trưng. Suy ra $p(x)$ có dạng $x-2,(x-2)^{2}$ hoặc $(x-2)^{3}$.
Lần lượt thay $A$ vào các đa thức, ta thấy $A-2 I \neq 0$ và $(A-2 I)^{2}=0$. Vậy $p(x)=(x-2)^{2}$.
(b). Thực hiện phép chia có dư, ta được $x^{2024}=(x-2)^{2} m(x)+a x+b$.
Thay $x=2$, ta được $2^{2024}=2 a+b$.
Lấy đạo hàm hai vế của $x^{2024}=(x-2)^{2} m(x)+a x+b$ và thay 2 vào các đa thức của 2 vế ta được
$$
2024.2^{2023}=a
$$
Suy ra $b=-2023.2^{2024}$. Khi đó $A^{2024}=2^{2023}(2024 A-4046 I)$.

Bài 6.5 (ĐH Trà Vinh).
(a) Ta có
$$
\begin{aligned}
1 & =\frac{5}{4}\left(1+x^{2}\right)-\frac{1}{4}\left(1+2 x+3 x^{2}\right)-\frac{1}{2}\left(-x+x^{2}\right) \\
x & =\frac{-1}{4}\left(1+x^{2}\right)+\frac{1}{4}\left(1+2 x+3 x^{2}\right)-\frac{1}{2}\left(-x+x^{2}\right) \\
x^{2} & =\frac{-1}{4}\left(1+x^{2}\right)+\frac{1}{4}\left(1+2 x+3 x^{2}\right)+\frac{1}{2}\left(-x+x^{2}\right)
\end{aligned}
$$
Từ đây suy ra
$$
\begin{aligned}
f(1) & =3-x+2 x^{2} \\
f(x) & =2+4 x+6 x^{2} \\
f\left(x^{2}\right) & =1+2 x+3 x^{2}
\end{aligned}
$$
Do đó ma trận của $f$ trong cơ sở chính tắc của $P_{2}(x)$ là
$$
A=\left(\begin{array}{ccc}
3 & 2 & 1 \\
-1 & 4 & 2 \\
2 & 6 & 3
\end{array}\right)
$$
(b) Giả sử có $u=a+b x+c x^{2}$ thỏa mãn $f(u)=v$. Khi đó $f\left(a+b x+c x^{2}\right)=$ $1+m x-5 x^{2}$, hay
$$
a\left(3-x+2 x^{2}\right)+b\left(2+4 x+6 x^{2}\right)+c\left(1+2 x+3 x^{2}\right)=1+m x-5 x^{2} .
$$
Xét hệ phương trình
$$
\left\{\begin{array}{l}
3 a+2 b+c=1 \\
-a+4 b+2 c=m \\
2 a+6 b+3 c=-5
\end{array}\right.
$$
Thế thì $v$ không thuộc $\operatorname{Im} f$ khi và chỉ khi hệ phương trình trên vô nghiệm. Ta có
$$
\left(\begin{array}{ccc|c}
3 & 2 & 1 & 1 \\
-1 & 4 & 2 & m \\
2 & 6 & 3 & -5
\end{array}\right) \leftrightarrow\left(\begin{array}{ccc|c}
3 & 2 & 1 & 1 \\
0 & 14 & 7 & 3 m+1 \\
0 & 0 & 0 & -m-6
\end{array}\right)
$$
Do đó hệ phương trình vô nghiệm khi và chỉ khi $-m-6 \neq 0$, tức là $m \neq-6$.
