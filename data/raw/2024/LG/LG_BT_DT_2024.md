Bài 2.1 (ĐH Mỏ-Địa chất). 
Giả sử $B=\left(b_{i j}\right)$, trong đó $b_{i j}$ bằng 1 nếu $j$ là nhân tử của $i$ và bằng 0 trong các trường hợp còn lại. Điều đó có nghĩa là ma trận này là ma trận tam giác với đường chéo chứa các số 1 . Khi đó, ma trận $A=\left(a_{i j}\right)$ sẽ bằng $A=B B^T$, trong đó $B^T$ là ma trận chuyển. Từ đó suy ra $\operatorname{det} A=(\operatorname{det} B)\left(\operatorname{det} B^T\right)=(\operatorname{det} B)^2=1$.

Bài 2.2 (ĐH Đồng Tháp). 
Khai triển định thức theo dòng cuối để được $\Delta_n=$ $a \Delta_{n-1}+\Delta_{n-2}$. Từ đó suy ra điều phải chứng minh.

Bài 2.3 (ĐH Tân Trào). 
Đặt $D_n(x)=\left|\begin{array}{cccccc}x & 1 & 0 & \cdots & 0 & 0 \\ n-1 & x & 2 & \cdots & 0 & 0 \\ 0 & n-2 & x & \cdots & 0 & 0 \\ . & . & . & \cdots & . & . \\ 0 & 0 & 0 & \cdots & x & n-1 \\ 0 & 0 & 0 & \cdots & 1 & x\end{array}\right|$. 
Ta có
$$
D_n(x)=(x+n-1)\left|\begin{array}{cccccc}
1 & 1 & 1 & \cdots & 1 & 1 \\
n-1 & x & 2 & \cdots & 0 & 0 \\
0 & n-2 & x & \cdots & 0 & 0 \\
\cdot & \cdot & \cdot & \cdots & \cdot & \cdot \\
0 & 0 & 0 & \cdots & x & n-1 \\
0 & 0 & 0 & \cdots & 1 & x
\end{array}\right|=(x+n-1) \Lambda .
$$
Thực hiện các biến đổi sơ cấp trên dòng và cột của $D$, ta có
$$
\Lambda=\left|\begin{array}{cccccc}
x-1 & 1 & 0 & \cdots & 0 & 0 \\
n-2 & x-1 & 2 & \cdots & 0 & 0 \\
0 & n-3 & x-1 & \cdots & 0 & 0 \\
\cdot & \cdot & \cdot & \cdots & \cdot & \cdot \\
0 & 0 & 0 & \cdots & x-1 & n-2 \\
0 & 0 & 0 & \cdots & 1 & x-1
\end{array}\right|_{n-1}=D_{n-1}(x-1) .
$$
Suy ra,
$$
D_n=(x+n-1) D_{n-1}(x-1)=(x+n-1)(x+n-3) D_{n-2}(x-2) .
$$
Do đó, khi $n=2 k$, thì
$$
D_{2 k}=\left(x^2-1\right)\left(x^2-9\right) \cdots\left[x^2-(2 k-1)^2\right] .
$$
Vậy, với $n=x=2024$ ta nhận được $D=\left(2024^2-1\right)\left(2024^2-3^2\right) \ldots\left(2024^2-\right.$ $\left.2023^2\right)$.

Bài 2.4 (ĐH Vinh). 
Từ định nghĩa định thức ta suy ra ma trận vuông có tất cả các phần tử đều là số nguyên thì định thức của ma trận đó cũng là số nguyên. Theo tính chất đồng dư, ta có $\operatorname{det} A \equiv \operatorname{det} B(\bmod 2)$, trong đó
$$
B=\left(\begin{array}{cccc}
0 & 1 & \ldots & 1 \\
1 & 0 & \ldots & 1 \\
\ldots & \ldots & \ldots & \ldots \\
1 & 1 & \ldots & 0
\end{array}\right)_{2024 \times 2024} .
$$
Ta kiểm tra được rằng
$$
B^2=\left(\begin{array}{cccc}
2023 & 2022 & \ldots & 2022 \\
2022 & 2023 & \ldots & 2022 \\
\ldots & \ldots & \ldots & \ldots \\
2022 & 2022 & \ldots & 2023
\end{array}\right)_{2024 \times 2024} .
$$
Ta có $\operatorname{det}\left(B^2\right) \equiv \operatorname{det}\left(I_{2024}\right)=1(\bmod 2)$, trong đó $I_{2024}$ ký hiệu là ma trận đơn vị cấp 2024. Hơn nữa, $\operatorname{det}\left(B^2\right)=(\operatorname{det} B)^2$ nên ta suy ra $\operatorname{det} B$ là một số nguyên lẻ. Điều này kéo theo $\operatorname{det} A$ cũng là một số nguyên lẻ. Do đó, $\operatorname{det} A \neq 0$, nghĩa là A là ma trận khả nghịch.

Bài 2.5 (ĐH Hải Phòng). 
Ta có $\operatorname{det} A=-4 x^2-16 x-12$. Khi đó
$$
\operatorname{rank} A=4 \Leftrightarrow \operatorname{det} A \neq 0 \Leftrightarrow x \neq-3,-1 .
$$
- Với $x=-3$ ta có
$$
A=\left[\begin{array}{cccc}
1 & -2 & -1 & 0 \\
0 & 1 & 0 & -1 \\
-1 & 0 & 1 & -2 \\
0 & -1 & 0 & 1
\end{array}\right] \sim\left[\begin{array}{cccc}
1 & -2 & -1 & 0 \\
0 & 1 & 0 & -1 \\
0 & 0 & 0 & -4 \\
0 & 0 & 0 & 0
\end{array}\right] \Rightarrow \operatorname{rank} A=3
$$
- Với $x=-1$ ta có
$$
A=\left[\begin{array}{llll}
1 & 0 & 1 & 0 \\
2 & 1 & 0 & 1 \\
1 & 0 & 1 & 0 \\
0 & 1 & 2 & 1
\end{array}\right] \sim\left[\begin{array}{cccc}
1 & 0 & 1 & 0 \\
0 & -1 & 2 & 1 \\
0 & 0 & 4 & 0 \\
0 & 0 & 0 & 0
\end{array}\right] \Rightarrow \operatorname{rank} A=3
$$
Vậy
$$
\operatorname{rank} A= \begin{cases}4, & \text { khi } x \neq-3,-1 \\ 3, & \text { khi } x=-3,-1\end{cases}
$$

Bài 2.6 (ĐH Trà Vinh). 
(a) Ta có $A^{-1}=A \Rightarrow A^2=I$. Từ đó
$$
(I-A)^2=A^2-2 A+I=2(I-A)
$$
dẫn đến $|\operatorname{det}(I-A)|^2=|\operatorname{det}(2(I-A))|=2^n|\operatorname{det}(I-A)|$. Từ đây có điều phải chứng minh.
(b) Ta có $A^{2 k+1}-A=A\left(A^{2 k}-I\right)$ nên
$$
\left|\operatorname{det}\left(A^{2 k+1}-A\right)\right|=\left|\operatorname{det}(A) \| \operatorname{det}\left(A^{2 k}-I\right)\right| .
$$
Vì $A^{-1}=4 A$ nên $I=4 A^2$, dẫn đến
$$
A^{2 k}-I=\left(\frac{1-4^k}{4^k}\right) I
$$
Do đó
$$
\left|\operatorname{det}\left(A^{2 k}-I\right)\right|=\left(\frac{4^k-1}{4^k}\right)^n
$$
Mặt khác, vì $A^2=4 I$ nên
$$
|\operatorname{det}(A)|=\frac{1}{2^n}
$$
Từ đây ta có điều phải chứng minh.

Bài 2.7 (ĐH Trà Vinh). 
Đặt $a_1 a_2 a_3=13 m, b_1 b_2 b_3=13 n, c_1 c_2 c_3=13 p$. Ta có
$$
\begin{aligned}
\left|\begin{array}{lll}
a_1 & a_2 & a_3 \\
b_1 & b_2 & b_3 \\
c_1 & c_2 & c_3
\end{array}\right| & =\left|\begin{array}{lll}
a_1 & a_2 & 100 a_1+10 a_2+a_3 \\
b_1 & b_2 & 100 b_1+10 b_2+b_3 \\
c_1 & c_2 & 100 c_1+10 c_2+c_3
\end{array}\right| \\
& =\left|\begin{array}{lll}
a_1 & a_2 & 13 m \\
b_1 & b_2 & 13 n \\
c_1 & c_2 & 13 p
\end{array}\right| \\
& =13\left|\begin{array}{lll}
a_1 & a_2 & m \\
b_1 & b_2 & n \\
c_1 & c_2 & p
\end{array}\right|
\end{aligned}
$$
chia hết cho 13 .