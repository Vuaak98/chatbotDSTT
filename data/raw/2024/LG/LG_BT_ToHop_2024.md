Bài 7.1 (ĐH Giao thông Vận tải). 
Theo giả thiết, ban đầu các cờ đỏ được cắm từng nhóm 3 cái liên tục và các nhóm được ngăn bởi các cờ xanh. Để thuận tiện ta gọi mỗi nhóm là một khúc và các cờ xanh là điểm tiếp nối của các khúc. Ta thấy rằng lá cờ xanh ở vị trí 1 có thể đổi chỗ cho 2 lá cờ đỏ ở vị trí 2 hoặc 3 trong khúc thứ nhất. Lá cờ xanh ở vị trí 1 chỉ có thể đổi chỗ cho
duy nhất một lá cờ đỏ ở giữa trong mỗi khúc mà nó không là điểm tiếp nối. Như vậy ta có tất cả 11 cách đổi chỗ lá cờ xanh ở vị trí số 1 . Tương tự lá cờ xanh ở vị trí 41 cũng có 11 cách đổi chỗ. Tiếp theo ta xét các lá cờ xanh còn lại. Mỗi lá cờ xanh như thế là điểm tiếp nối của hai khúc nào đấy và nó có thể đổi chỗ cho 4 cờ đỏ trong 2 khúc này. Trong 8 khúc còn lại mà cờ xanh này không là điểm tiếp nối thì nó chỉ có thể đổi chỗ cho duy nhất lá cờ đỏ ở giữa. Như vậy mỗi lá cờ xanh ở các vị trí $5,9, \ldots, 37$ có 12 cách đổi chỗ. Tổng số cách đổi chỗ của các lá cờ là $2.11+9.12=130$ cách.

Bài 7.2 (ĐH Tân Trào).
![](https://cdn.mathpix.com/cropped/2025_06_27_004437f0d8a9f52bde4fg-5.jpg?height=315&width=1426&top_left_y=993&top_left_x=349)
- Dễ dàng thấy rằng $R_{1}=1, R_{2}=3$ và $R_{3}=5, R_{4}=11$.
- Khi chọn hình chữ nhật có kích thước $2 \times 1$ để xếp vào ô đầu tiên $A C D H$, thì phần còn lại có $R_{n-1}$ cách chia.
- Khi chọn hình chữ nhật có kích thước $1 \times 2$ để xếp vào ô đầu tiên $B C E F$ hoặc $A B F G$, thì phần còn lại có $R_{n-2}$ cách chia.
- Khi chọn hình chữ nhật có kích thước $2 \times 2$ để xếp vào ô đầu tiên $A C E G$, thì phần còn lại cũng sẽ có $R_{n-2}$ cách chia.
- Suy ra, theo nguyên lý cộng, số cách chia thỏa mãn yêu cầu bài ra là (công thức truy hồi) $R_{n}=R_{n-1}+2 R_{n-2}$, trong đó $R_{1}=1, R_{2}=3$.
- Phương trình đặc trưng $\lambda^{2}-\lambda-2=0$ có hai nghiệm phân biệt $\lambda_{1}=-1$, $\lambda_{2}=2$.
Ta tìm $x_{1}, x_{2}$ sao cho
$$
\begin{equation*}
R_{n}=x_{1} \lambda_{1}^{n}+x_{2} \lambda_{2}^{n} \tag{4}
\end{equation*}
$$
Thay $\lambda_{1}=-1, \lambda_{2}=2$ vào phương trình (1), ta nhận được hệ phương trình
$$
\left\{\begin{array}{l}
x_{1}+2 x_{2}=1 \\
x_{1}+4 x_{2}=3
\end{array} \rightarrow x_{1}=\frac{1}{3}, x_{2}=\frac{2}{3}\right.
$$
Suy ra, $\quad R_{n}=\frac{1}{3}\left[(-1)^{n}+2^{n+1}\right]$, với $0<n \in \mathbb{N}$.

Bài 7.3 (ĐH Vinh).
(a) Ký hiệu 4 chàng trai là $A, B, C, D$ và 4 cô gái tương ứng theo cặp đôi là $a, b, c, d$.
Chàng trai $A$ có 3 cách chọn phong bì không ghi tên người yêu mình (là $b, c, d$ ).
Không mất tính tổng quát, xét $A$ chọn được phong bì ghi tên cô gái $b$, ta viết cặp $A b$. Khi đó,
- Nếu $B$ chọn phong bì ghi tên $a$ để được cặp $B a$ thì 02 cặp còn lại sẽ là $C d$ và $D c$.
- Nếu $B$ chọn phong bì ghi tên $c$ để được cặp $B c$ thì 02 cặp còn lại sẽ là $C d$ và $D a$.
- Nếu $B$ chọn phong bì ghi tên $d$ để được cặp $B d$ thì 02 cặp còn lại sẽ là $C a$ và $D c$.
Vậy, số kết quả có thể xảy ra để không có chàng trai nào chọn đúng phong bì ghi tên người yêu của mình là $3 \times 3=9$.
(b) Ta xét bài toán tổng quát cho $n$ cặp đôi và gọi $D_{n}$ là số kết quả có thể xảy ra để không có chàng trai nào chọn đúng phong bì ghi tên người yêu của mình. Dễ thấy $D_{1}=0$ và $D_{2}=1$.
Giả sử chàng trai thứ $i$ chọn được phong bì thứ $a_{i}\left(1 \leq a_{i} \leq n, i=\overline{1, n}\right.$, $a_{i} \neq i$ ). Ta sẽ lập công thức truy hồi của $D_{n}$ :
- $a_{n}$ có $n-1$ cách chọn từ $\{1,2, \ldots, n-1\}$.
- Giả sử $a_{n}=k(1 \leq k \leq n-1)$ :
TH1: $a_{k}=n$.
Khi đó $\left(a_{1}, a_{2}, \ldots, a_{k-1}, a_{k+1}, \ldots, a_{n-1}\right)$ chọn từ tập $\{1,2, \ldots, k-1, k+$ $1, \ldots, n-1\}$. Suy ra số kết quả có thể xảy ra trong trường hợp này là $D_{n-2}$.
TH2: $a_{k} \neq n$.
Khi đó $\left(a_{1}, a_{2}, \ldots, a_{k-1}, a_{k}, a_{k+1}, \ldots, a_{n-1}\right)$ lấy từ $\{1.2, \ldots, n-1\}$. Suy ra số kết quả có thể xảy ra trong trường hợp này là $D_{n-1}$.
Vì vậy ta có công thức:
$$
D_{n}=(n-1)\left(D_{n-1}+D_{n-2}\right) .
$$
Ta xác định $D_{10}$ theo cách truy hồi:
$$
\begin{aligned}
D_{1} & =0, D_{2}=1, D_{3}=2\left(D_{1}+D_{2}\right)=2 \\
D_{4} & =3\left(D_{3}+D_{2}\right)=3(2+1)=9 \\
D_{5} & =4\left(D_{4}+D_{3}\right)=4(9+2)=44 \\
D_{6} & =5\left(D_{5}+D_{4}\right)=5(44+9)=265 \\
D_{7} & =6\left(D_{6}+D_{5}\right)=6(265+44)=1854 \\
D_{8} & =7\left(D_{7}+D_{6}\right)=14833 \\
D_{9} & =8\left(D_{8}+D_{7}\right)=133496 \\
D_{10} & =9\left(D_{9}+D_{8}\right)=1334961
\end{aligned}
$$
Vậy đáp số là 1334961 .
