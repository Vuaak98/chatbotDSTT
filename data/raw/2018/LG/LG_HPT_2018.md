Bài 3.1 (ĐH Kiến Trúc Hà Nội). 
Hệ phương trình được viết lại như sau:
$$
\left\{\begin{array}{l}
\left(2 a_{11}-1\right) x_1+2 a_{12} x_2+\cdots+2 a_{1 n} x_n=0 \\
2^2 a_{21} x_1+\left(2^2 a_{22}-1\right) x_2+\cdots+2^2 a_{2 n} x_n=0 \\
\quad \ldots \ldots \ldots \ldots \ldots \ldots \ldots \ldots \ldots \ldots \ldots \ldots \ldots \ldots \\
2^n a_{n 1} x_1+2^n a_{n 2} x_2+\cdots+\left(2^n a_{n n}-1\right) x_n=0
\end{array}\right.
$$
Gọi $A_n$ là ma trận hệ số của hệ phương trình.
Do các phần tử trên đường chéo chính của ma trận $A_n$ đều chia 2 dư 1 , các phẩn tử nằm ngoài đường chéo chính của $A_n$ đểu chia hết cho 2 nên ta suy ra định thức của ma trận $A_n$ cùng tính chẵn lẻ với định thức của ma trận đơn vị $I_n$. Mặt khác ta có $\operatorname{det}\left(I_n\right)=1$ là số lẻ, do đó $\operatorname{det}\left(A_n\right)$ cũng là một số nguyên lẻ, do vậy $\operatorname{det}\left(A_n\right) \neq 0$. Từ đó suy ra hệ phương trình đã cho chỉ có nghiệm tầm thường.

Bài 3.2 (HV Kỹ thuật Quân sự). 
(a) Dễ thấy nghiệm (1) là nghiệm (2). Ngược lại, giả sử $x$ là nghiệm (2), ta có $\left(A+A^2+\ldots+A^{2017}+A^{2018}\right) x=$ $\left(E+A+\ldots+A^{\text {2017 }}\right) A x=0$, nhưng dễ thấy $E+A+\ldots+A^{2017}=(E-A)^{-1}$là ma trận khả nghịch nên $A x=0$.
b) Ta có hệ (1) và (2) có cùng không gian nghiệm. Giả sử dim $(N)=r$ thì $\operatorname{rank}(A)=\operatorname{rank}\left(A+A^2+\ldots+A^{2017}\right)=n-r$

Bài 3.3 (ĐH Sư phạm Kỹ thuật Vĩnh Long). 
Ta có
$$
\begin{aligned}
\operatorname{det}\left[\begin{array}{rrrr}
20172017 & 20172017 & 20182018 & 20172017 \\
20172017 & 20162016 & 20192019 & 20162016 \\
20192019 & 20152015 & 20182018 & 20172017 \\
20202020 & 20162016 & 20202020 & 20192019
\end{array}\right] & \stackrel{\text { mods }}{\equiv} \operatorname{det}\left[\begin{array}{llll}
2 & 2 & 3 & 2 \\
2 & 1 & 4 & 1 \\
4 & 0 & 3 & 2 \\
0 & 1 & 0 & 4
\end{array}\right] \\
& =46 \stackrel{\text { mods }}{\equiv} 1 .
\end{aligned}
$$
Suy ra
$$
\operatorname{det}\left[\begin{array}{llll}
20172017 & 20172017 & 20182018 & 20172017 \\
20172017 & 20162016 & 20192019 & 20162016 \\
20192019 & 20152015 & 20182018 & 20172017 \\
20202020 & 20162016 & 20202020 & 20192019
\end{array}\right] \neq 0
$$
Vậy hệ có nghiệm duy nhất là nghiệm tầm thường $(0,0,0,0)$.

Bài 3.4 (ĐH Tây Bắc). 
Gọi $D$ là định thức của ma trận hệ số của hệ phương trình đã cho. Ta có:
$$
D=\left|\begin{array}{cccc}
a_1 & 1 & 1 & 1 \\
1 & a_2 & 1 & 1 \\
1 & 1 & a_3 & 1 \\
1 & 1 & 1 & a_4
\end{array}\right|
$$
Lấy các dòng $i(i=2,3,4)$ trừ đi đòng 1 rồi đưa các nhân tử chung ( $1-a_i$ ) của cột thứ $i(i=1,2,3,4)$ ra ngoài thì được:
$$
D=\prod_{i=1}^4\left(1-a_i\right)\left|\begin{array}{cccc}
\frac{a_1}{1-a_1} & \frac{1}{1-a_2} & \frac{1}{1-a_3} & \frac{1}{1-a_4} \\
1 & -1 & 0 & 0 \\
1 & 0 & -1 & 0 \\
1 & 0 & 0 & -1
\end{array}\right|
$$
Cộng tất cả các cột vào cột 1 thì được:
$$
\begin{aligned}
D & =\prod_{i=1}^4\left(1-a_i\right)\left|\begin{array}{cccc}
\frac{a_1}{1-a_1}+\sum_{i=2}^4 \frac{1}{1-a_i} & \frac{1}{1-a_2} & \frac{1}{1-a_3} & \frac{1}{1-a_4} \\
0 & -1 & 0 & 0 \\
0 & 0 & -1 & 0 \\
0 & 0 & 0 & -1
\end{array}\right| \\
& =-\prod_{i=1}^4\left(1-a_i\right)\left(\frac{a_1}{1-a_1}+\sum_{i=2}^4 \frac{1}{1-a_i}\right) \\
& <0
\end{aligned}
$$Vậy hệ phương trình đã cho có duy nhất nghiệm tầm thường.

Bài 3.5 (ĐH Giao thông Vận tải). 
Ký hiệu sản lượng của các xí nghiệp là $x_1, x_2, x_3, x_4$ và không mất tính tổng quát ta giả sử $x_1 \geqslant x_2 \geqslant x_3 \geqslant x_4$. Ký hiệu $x_5$ là nhu cầu nước sinh hoạt hàng ngày của toàn thành phố. Nếu xí nghiệp thứ nhất được bảo dưỡng theo định kỳ thì lượng nước bị thiếu hụt là $\alpha_1=0,5 x_1-0,2 x_2-0,15 x_3-0,1 x_4$. Tương tự các xí nghiệp thứ $2,3,4$ được bảo dưỡng theo định kỳ thì lượng nước bị thiếu hụt tương ứng là $\alpha_2=0,5 x_2-0,2 x_1-0,15 x_3-0,1 x_4 ; \alpha_3=0,5 x_3-0,2 x_1-0,15 x_2-0,1 x_4$; $\alpha_4=0,5 x_4-0,2 x_1-0,15 x_2-0,1 x_3$. Tứ $x_1 \geqslant x_2 \geqslant x_3 \geqslant x_4$ ta suy ra được $\alpha_1 \geqslant \alpha_2 \geqslant \alpha_3 \geqslant \alpha_4$. Đối chiếu với giả thiết ta thu được dãy $\left\{\alpha_1, \alpha_2, \alpha_3, \alpha_4\right\}$ chính là $\{56,14,-12,-36\}$. Từ đó ta lập được hệ phương trình tuyến tính
$$
\left\{\begin{array}{l}
0,5 x_1-0,2 x_2-0,15 x_3-0,1 x_4=56 \\
-0,2 x_1+0,5 x_2-0,15 x_3-0,1 x_4=14 \\
-0,2 x_1-0,15 x_2+0,5 x_3-0,1 x_4=-12 \\
-0,2 x_1-0,15 x_2-0,1 x_3+0,5 x_4=-36
\end{array}\right.
$$
Giải hệ theo phép khử Gauss ta thu được kết quả: $x_1=300, x_2=240, x_3=$ $200, x_4=160$. Từ đó ta tính được $x_5=x_1+x_2+x_3+x_4=900$.
Ghi chú. Ta có thể giải bài toán bằng cách lập hệ phương trình tuyến tính
$$
\left\{\begin{array}{l}
x_1+x_2+x_3+x_4-x_5=0 \\
0,5 x_1+1,2 x_2+1,15 x_3+1,1 x_4-x_5=-56 \\
1,2 x_1+0,5 x_2+1,15 x_3+1,1 x_4-x_5=-14 \\
1,2 x_1+1,15 x_2+0,5 x_3+1,1 x_4-x_5=12 \\
1,2 x_1+1,15 x_2+1,1 x_3+0,5 x_4-x_5=36
\end{array}\right.
$$
Giải hệ theo phép khử Gauss ta thu được kết quả: $x_1=300, x_2=240, x_3=$ $200, x_4=160, x_5=900$.