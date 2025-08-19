Bài 1.1 (ĐH Công nghệ Thông tin). 
Xét hệ phương trình tuyến tính $(A+B+$ $I) X=0$ hay $(B+I) X=-A X$. Khi đó
$$
-A^{2} X=A(B+I) X=(A B+A) X=(B A+A) X=(B+I) A X=-(B+I)^{2} X
$$
Tiếp tục quá trình như trên, ta có $(B+I)^{k} X=(-1)^{k} A^{k} X$. Vì $A^{2024}=I$ nên $(B+I)^{2024} X=X$ hay $\left((B+I)^{2024}-I\right) X=0$. Mặt khác $\left(B^{2023}-I\right) X=0$ (vì $B^{2023}=I$ ).
Xét các đa thức $p(t)=(t+1)^{2024}-1$ và $q(t)=t^{2023}-1$. Nghiệm của đa thức $p(t)$ có dạng $-1+\cos \frac{2 k \pi}{2024}+i \sin \frac{2 k \pi}{2024}$ với $k=0,1, \ldots, 2023$. Nghiệm của đa thức $q(t)$ có dạng $\cos \frac{2 m \pi}{2023}+i \sin \frac{2 m \pi}{2023}$ với $m=0,1, \ldots, 2022$. Ta thấy rằng $p(t)$ và $q(t)$ không có nghiệm chung. Như vậy $p(t)$ và $q(t)$ là 2 đa thức nguyên tố cùng nhau. Khi đó tồn tại các đa thức $r(t), s(t)$ sao cho
$$
r(t) p(t)+s(t) q(t)=1
$$
Khi đó $X=(r(B) p(B)+s(B) q(B)) X=r(B)(p(B) X)+s(B)(q(B) X)=0$. Như vậy hệ phương trình tuyến tính thuần nhất $(A+B+I) X=0$ chỉ có nghiệm tầm thường. Do đó $A+B+I$ khả nghịch.

Bài 1.2 (ĐH Công nghệ Thông tin). 
Ta cần tìm các ma trận $S, T$ sao cho
$$
M=S^{-1} N S, P=T^{-1} Q T
$$
Ta chọn các ma trận
$$
S=\frac{1}{\sqrt{2}}\left[\begin{array}{cc}
I_{n} & I_{n} \\
I_{n} & -I_{n}
\end{array}\right] \text { và } T=\frac{1}{\sqrt{2}}\left[\begin{array}{cc}
I_{n} & i I_{n} \\
-i I_{n} & -I_{n}
\end{array}\right] \text {. }
$$

Bài 1.3 (ĐH Công nghệ Thông tin). 
Ta thấy $a=b=0$ không thỏa mãn bài toán.
Giả sử $a^{2}+b^{2} \neq 0$, nghĩa là $a, b$ không đồng thời bằng 0 . Khi đó
$$
\left[\begin{array}{cc}
a & -b \\
b & a
\end{array}\right]=\sqrt{a^{2}+b^{2}}\left[\begin{array}{cc}
\cos t & -\sin t \\
\sin t & \cos t
\end{array}\right]
$$
và $\left[\begin{array}{cc}a & -b \\ b & a\end{array}\right]^{4}=\left(a^{2}+b^{2}\right)^{2}\left[\begin{array}{cc}\cos 4 t & -\sin 4 t \\ \sin 4 t & \cos 4 t\end{array}\right]$. Suy ra $a^{2}+b^{2}=\sqrt{2}$ và dẫn đến
$$
\cos t=\frac{1}{\sqrt[4]{2}}, \cos 4 t=\frac{\sqrt{3}}{2}
$$
Ta có phương trình
$$
2\left(\sqrt{2} a^{2}-1\right)^{2}-1=\frac{\sqrt{3}}{2}
$$
có nghiệm $a, b$ thỏa mãn
$$
a^{2}=\frac{2 \sqrt{2}+(1+\sqrt{3})}{4} ; b^{2}=\frac{2 \sqrt{2}-(1+\sqrt{3})}{4}
$$
hoặc
$$
a^{2}=\frac{2 \sqrt{2}-(1+\sqrt{3})}{4} ; b^{2}=\frac{2 \sqrt{2}+(1+\sqrt{3})}{4} .
$$

Bài 1.4 (ĐH Giao thông Vận tải). 
Đặt $A=3 I+M$ với ma trận $M$ là $M=$ $\left(\begin{array}{cccc}0 & 0 & 1 & -1 \\ 0 & -1 & 0 & -1 \\ 0 & 1 & 0 & 1 \\ 0 & 1 & 0 & 1\end{array}\right)$. Tính toán trực tiếp ta thu được $M^{2}=0$. Do đó
$$
\begin{aligned}
A^{2024} & =(3 I+M)^{2024}=3^{2024} I+3^{2023} 2024 M=3^{2023}(3 I+2024 M) \\
& =3^{2023}\left(\begin{array}{cccc}
3 & 0 & 2024 & -2024 \\
0 & -2021 & 0 & -2024 \\
0 & 2024 & 3 & 2024 \\
0 & 2024 & 0 & 2027
\end{array}\right)
\end{aligned}
$$

Bài 1.5 (ĐH Đồng Tháp). 
Ta có
$$
A^{-1}=\left(\begin{array}{cccc}
1 & 1 & 1 & 1 \\
0 & 1 & 1 & 1 \\
0 & 0 & 1 & 1 \\
0 & 0 & 0 & 1
\end{array}\right)
$$

Bài 1.6 (ĐH Tân Trào). 
Ta có $A=24 I+5 B, B=\left[\begin{array}{ccc}4 & -5 & 2 \\ 5 & -7 & 3 \\ 6 & -9 & 4\end{array}\right] \rightarrow A^n=(24 I+$ $5 B)^n$.
$B^3=B^2=\left[\begin{array}{lll}3 & -3 & 1 \\ 3 & -3 & 1 \\ 3 & -3 & 1\end{array}\right]$ Dễ thấy, $B^n=B^2$ với mọi $n \geq 2$ (Chứng minh bằng quy nạp theo $k \in \mathbb{N}, k \geq 2$ ).
Khi đó ta có:
$$
\begin{aligned}
A^n & =\sum_{k=0}^n\binom{n}{k}(24 I)^{n-k}(5 B)^k=24^n I+n 24^{n-1} 5 B+B^2 \sum_{k=2}^n\binom{n}{k} 24^{n-k} 5^k \\
& =24^n I+5 n 24^{n-1} B+B^2\left[\sum_{k=0}^n\binom{n}{k} 24^{n-k} 5^k-24^n-5 n 24^{n-1}\right] \\
& =24^n I+5 n 24^{n-1} B+\left(29^n-24^n-5 n 24^{n-1}\right) B^2 .
\end{aligned}
$$
Tổng các phần tử trên đường chéo chính của $B, B^2$ đều có giá trị là 1 . Do đó $S=29^n+2 \times 24^n$.