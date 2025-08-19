Bài 4.1 (ĐH Giao thông Vận tải). 
Ánh xạ $f$ đã cho có thể mô tả dưới dạng ma trận $f(x)=A x$ với $x$ ở dạng cột và
$$
A=\left(\begin{array}{ccc}
0 & 0 & 1 \\
2 & 1 & -2 \\
1 & 0 & 0
\end{array}\right)
$$
Tính toán trực tiếp chúng ta có
$$
A^2=\left(\begin{array}{ccc}
0 & 0 & 1 \\
2 & 1 & -2 \\
1 & 0 & 0
\end{array}\right)\left(\begin{array}{ccc}
0 & 0 & 1 \\
2 & 1 & -2 \\
1 & 0 & 0
\end{array}\right)=\left(\begin{array}{lll}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{array}\right)
$$
hay là $A^2=I$.
Sử dụng $A^2=I$ ta có biến đổi
$$
f\left(-u_k+u_{k+1}\right)=3 u_k \Leftrightarrow A\left(-u_k+u_{k+1}\right)=3 u_k \Leftrightarrow-u_k+u_{k+1}=3 A u_k .
$$
Như vậy $u_{k+1}=(I+3 A) u_k$ và ta suy ra $u_{2018}=(I+3 A)^{2018} u_0$.
Ta có
$$
\begin{aligned}
(I+3 A)^{2018}= & \sum_{k=0}^{2018} C_{2018}^k 3^k A^k \\
= & \left(C_{2018}^0+3^2 C_{2018}^2+\ldots+3^{2018} C_{2018}^{2018}\right) I \\
& +\left(3 C_{2018}^1+3^3 C_{2018}^3+\ldots+3^{2017} C_{2018}^{2017}\right) A \\
= & \frac{(1+3)^{2018}+(1-3)^{2018}}{2} I+\frac{(1+3)^{2018}-(1-3)^{2018}}{2} A \\
= & \frac{4^{2018}+2^{2018}}{2} I+\frac{4^{2018}-2^{2018}}{2} A \\
= & 2^{2017}\left(\begin{array}{ccc}
k+1 & 0 & k-1 \\
2 k-2 & 2 k & -2 k+2 \\
k-1 & 0 & k+1
\end{array}\right)
\end{aligned}
$$
với $k=2^{2018}$. Từ đó ta thu được
$$
u_{2018}=(I+3 A)^{2018} u_0=2^{2017}\left(\begin{array}{ccc}
k+1 & 0 & k-1 \\
2 k-2 & 2 k & -2 k+2 \\
k-1 & 0 & k+1
\end{array}\right)\left(\begin{array}{l}
1 \\
2 \\
3
\end{array}\right)=2^{2018}\left(\begin{array}{c}
2 k-1 \\
2 \\
2 k+1
\end{array}\right) .
$$

Bài 4.2 (ĐH Quy Nhơn). 
(a) Ta có det $T=(-1)^n c_1 \ldots c_{n+1}$ và $T^n=c_1 \ldots c_n I$. 
(b) Theo Câu a), $\Phi$ là đẳng cấu.

Bài 4.3 (Trường sĩ quan Không quân). 
Giả sử $\lambda$ là giá trị riêng của $\varphi \psi$, tức là tồn tại véc tớ $v \neq 0$ sao cho $\varphi \psi(v)=\lambda v$. Khi đó, ta có $\psi \varphi(\psi(v))=\psi(\varphi \psi(v))=$ $\lambda \psi(v)$. Do đó, nếu $\psi(v) \neq 0$ thì $\lambda$ là giá trị riêng của $\psi \varphi$. Trong trường hợp $\psi(v)=0$ thì $\varphi \psi(v)=\varphi(\psi(v))=0$. Do vây, từ $\varphi \psi(v)=\lambda v$ và $v \neq 0$, ta thu được $\lambda=0$. Điểu này nói lên rằng $\operatorname{det}(B A)=0$ trong đó $A, B$ là ma trận biểu diễn của $\varphi$ và $\psi$. Mặt khác $0=\operatorname{det}(B A)=\operatorname{det}(B) \cdot \operatorname{det}(A)=\operatorname{det}(A B)$. Do vậy $\lambda=0$ cũng là giá trị riêng của $A B$ và suy ra $\lambda=0$ là giá trị riêng của $\psi \varphi$. Điều ngược lại được lập luận tương tự.

Bài 4.4 (ĐH Sư phạm Hà Nội 2). 
Xét các ma trận có dạng
- Các ma trận dạng $E_{11}-E_{i i}, i=2, \ldots, n$ có $E_{11}-E_{i i}=E_{1 i} E_{i 1}-E_{i 1} E_{1 i}$. Do đó $E_{11}-E_{i i}, i=2, \ldots, n$ nằm trong S .
- Các ma trận dạng $E_{i k}, i \neq k$ có $E_{i k}=E_{i 1} E_{1 k}-E_{1 k} E_{i 1}$. Do đó $E_{i k}, i \neq k$ nằm trong S .
Do đó $S$ chứa hệ gồm $(n-1)+n(n-1)=n^2-1$ ma trận độc lập tuyến tính (cần chứng minh tính chất độc lập tuyến tính).
Mặt khác mọi ma trận $M$ thuộc $S$ được sinh bởi các ma trận dạng $A B-B A$, với các $A, B \in \operatorname{Mat}(n, K)$ nên $\operatorname{tr}(M)=0$. Do đó $I_n$ không nằm trong S , vì vậy $\operatorname{dim} S \leq n^2-1$. Kết hợp trên ta có $\operatorname{dim} S=n^2-1$.
Kí hiệu $\mathrm{ZT}(\mathrm{n})$ là tập các ma trận vuông cấp n có vết bằng không. Từ nhận xét trên ta có $S \subset Z T(n)$, kết hợp với $\operatorname{dim}(Z T(n)) \leq n^2-1$ ta có ngay rằng $S$ chính là tập các ma trận có vết bằng không.

Bài 4.5 (ĐH Sư phạm Hà Nội 2). 
Xét một quan hệ tuyến tính giữa hữu hạn các phẩn tử của tập $f_0, f_1, f_2, \ldots$, chẳng hạn:
$$
\alpha_1 f_{n_1}+\ldots+\alpha_p f_{n_p}=0, \alpha_1, \ldots, \alpha_p \in \mathbf{R}
$$
Không mất tính tổng quát, ta giả sử $n_1<n_2<\ldots<n_p$. Ta chứng minh quy nạp theo p là $\alpha_1=\ldots=\alpha_p=0$.
Khị $p=1$, nếu $\alpha_1 \neq 0$ thì vế trái là một đa thức bậc đúng bằng $n_1$, nên nó không thể bằng đa thức 0 . Vô lí. Vậy $\alpha_1=0$.
Giả sử khẳng định đúng với $p-1$. Xét trường hợp p đa thức. Nếu $\alpha_p \neq 0$ thì $\alpha_1 f_{m_1}+\ldots+\alpha_p f_{n_p}$ là đa thức bậc đúng bằng $n_p$. Do đó nó khác 0 . Vô lí. Vậy $\alpha_p=0$.
Theo giả thiết quy nạp, ta có $\alpha_1 f_{n_1}+\ldots+\alpha_p f_{n_p}=0$ thì $\alpha_1=\ldots=\alpha_p=0$. Vậy hệ đã cho độc lập tuyến tính.