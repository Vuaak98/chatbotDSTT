Bài 5.1 (HV Kỹ thuật Quân sự). 
Gọi $A$ là ma trận của một toán tử trong cơ sở nào đó. Dễ thấy $\lambda_0$ là nghiệm đơn của đa thức đặc trưng thì ứng với nó có đúng 1 vector riêng $e_1$, bổ sung $e_2, \ldots, e_n$ thành cơ sở mới không gian. Trong cơ sở mới này ta có
$$
\bar{A}=\left[\begin{array}{cccc}
\lambda_0 & b_{12} & \ldots & b_{1 n} \\
0 & b_{2 n} & \ldots & b_{2 n} \\
\ldots & \ldots & \ldots & \ldots \\
0 & b_{n 2} & \ldots & b_{n n}
\end{array}\right]
$$
Khi đó
$$
\operatorname{rank}\left(A-\lambda_0 E\right)=\operatorname{rank}\left(\bar{A}-\lambda_0 E\right)=n-1
$$
vì
$$
\left|\begin{array}{ccc}
b_{n 2}-\lambda_0 & \ldots & b_{2 n} \\
\ldots & \ldots & \ldots \\
b_{n 2} & \ldots & b_{n n-\lambda_0}
\end{array}\right| \neq 0
$$
do $\lambda_0$ là nghiệm đơn phương trình đặc trưng.

Bài 5.2 (ĐH Mỏ địa chất). 
Vì ma trận đối xứng nên tất cả các giá trị riêng của nó đều là thực. Tổng tất cả các phẩn tử trên đường chéo của ma trận là số dương và bằng tổng tất cả các giá trị riêng của nó - vết của ma trận. Vì vết bất biến qua phép biến đối cơ sở nên tống tất cả các giá trị riêng là số dương. Vì vậy trong tất cả các giá trị riêng của ma trận đã cho có ít nhất một giá trị riêng là dương.

Bài 5.3 (ĐH Quy Nhơn). 
Giả sử $A$ có $k$ giá trị riêng phẩn biệt $\lambda_1, \ldots, \lambda_k$. Áp dụng phép nội suy Lagrange, tổn tại một đa thức $p$ sao cho $p\left(\lambda_i\right)=\bar{\lambda}_i$ với mọi $i=1, \ldots, k$. Suy ra $U^H p(A) U=p(D)$, vói $p(D)$ là ma trận dường chéo với các phẩn tử chéo là một trong các $p\left(\lambda_i\right)=\bar{\lambda}_i$. Do đó $p(D)=D^H$. Suy ra $p(A)=A^H$.

Bài 5.4 (ĐH Sư phạm Kỹ thuật Hưng Yên). 
Giả sử $\lambda$ là giá trị riêng và $v=$ $\left(v_1, v_2, \ldots, v_n\right)^t \neq(0,0, \ldots, 0)^t$ là vector riêng tương ứng. Ta có
$$
\begin{aligned}
& A v=\left(\begin{array}{c}
2 v_1-v_2 \\
-v_1+2 v_2-v_3 \\
-v_2+2 v_3-v_4 \\
\cdots \\
-v_{n-2}+2 v_{n-1}-v_n \\
-v_{n-1}+2 v_n
\end{array}\right), \\
& \langle A v, v\rangle=\left(2 v_1^2-v_1 v_2\right)+\left(-v_1 v_2+2 v_2^2-v_2 v_3\right)+\cdots \\
& +\left(-v_{n-2} v_{n-1}+2 v_{n-1}^2-v_{n-1} v_n\right)+\left(-v_{n-1} v_n+2 v_n^2\right) \\
& =v_1^2+\left(v_1-v_2\right)^2+\left(v_2-v_3\right)^2+\cdots+\left(v_{n-1}-v_n\right)^2+v_n^2>0 .
\end{aligned}
$$Mặt khác $\langle A v, v\rangle=\langle\lambda v, v\rangle=\lambda\langle v, v\rangle=\lambda\|v\|^2$, mà $\|v\|^2=\left(v_1^2+v_2^2+\cdots+\right.$ $\left.v_n^2\right)^{\frac{1}{2}}>0$.
Do đó suy ra $\lambda>0$

Bài 5.5 (ĐH Tây Bắc). 
(a) Ta có:
$$
|A-\lambda I|=\left|\begin{array}{ccc}
-1-\lambda & -3 & 0 \\
-3 & 2-\lambda & 1 \\
0 & 1 & -1-\lambda
\end{array}\right|=(1+\lambda)(3+\lambda)(4-\lambda) .
$$
Suy ra $A$ có 3 giá trị riêng là $\lambda=-1 ; \lambda=-3 ; \lambda=4$.
(b) Nếu $\lambda$ là trị riêng của $A$ thì $|A-\lambda I|=0$ suy ra:
$$
\begin{aligned}
\left|A^n-\lambda^n I\right| & =\left|(A-\lambda I)\left(A^{n-1}+\lambda A^{n-2}+\ldots+\lambda^{n-1} I\right)\right| \\
& =|A-\lambda I|\left|A^{n-1}+\lambda A^{n-2}+\ldots+\lambda^{n-1} I\right| \\
& =0 .
\end{aligned}
$$

Vậy $\lambda^n$ là trị riêng của $A^n$.
(c) Do -1 là trị riêng của $A$ nên $(-1)^{2013}$ là trị riêng của $A^{2013}$ vậy
$$
\left|A^{2013}+I\right|=\left|A^{2013}-(-1)^{2013} I\right|=0
$$
Suy ra
$$
\left|A^4+A^{2017}\right|=\left|A^4\right| \cdot\left|A^{2013}+I\right|=0
$$