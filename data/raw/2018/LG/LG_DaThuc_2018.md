Bài 6.1 (ĐH Giao thông Vận tải). 
Từ giả thiết ta suy ra $P(x)$ có biểu diễn dưới dạng $P(x)=\alpha \prod_{i=1}^n\left(x-a_i\right)$. Từ đó ta có $P^{\prime}\left(a_1\right)=\alpha \prod_{i=2}^n\left(a_i-a_1\right)$. Theo giả thiết ta có với mỗi $i \geqslant 2$
$$
0<a_i-a_1=2 a_i-2 b-\left(a_i-a_2\right)-\left(a_1+a_2-2 b\right)<2\left(a_i-b\right) .
$$
Như vậy
$$
\begin{aligned}
|P(b)| & =\left|b-a_1\right| \prod_{i=2}^n\left|b-a_i\right| \\
& \geqslant\left|b-a_1\right| \prod_{i=2}^n \frac{1}{2}\left(a_i-a_1\right)=2^{-(n-1)}\left|b-a_1\right|\left|P^{\prime}\left(a_i\right)\right|
\end{aligned}
$$
Từ đó ta thu được điểu phải chứng minh.

Bài 6.2 (ĐH Kiến Trúc Hà Nội). 
(a)
Bước 1: Chứng minh hệ $B_a$ độc lập tuyến tính.
Bước 2: Hệ $B_a$ có $n+1$ phẩn tử bằng với số chiểu của không gian $P_n[x]$. Từ đó suy ra $B_a$ là một cơ sở của $P_n[x]$.
(b) Ta có:
$$
(x-b)^k=((a-b)+(x-a))^k=\sum_{m=0}^k C_k^m(a-b)^{k-m}(x-a)^m .
$$
Do đó: ma trận chuyến cơ sở từ cơ sồ $B_a$ sang cơ sở $B_b$ là:
$$
\left(\begin{array}{ccccc}
C_0^0 & C_1^0(a-b) & C_2^0(a-b)^2 & \cdots & C_n^0(a-b)^n \\
0 & C_1^1 & C_2^1(a-b) & \cdots & C_n^1(a-b)^{n-1} \\
0 & 0 & C_2^2 & \cdots & C_n^2(a-b)^{n-2} \\
\ldots & \ldots & \cdots & \cdots & \\
0 & 0 & 0 & \cdots & C_n^n
\end{array}\right)
$$


Bài 6.3 (ĐH Kiến Trúc Hà Nội). 
Xét đa thức $Q(x)=P(x)-x$ có bậc 2018. Ta có:
$$
Q(0)=-\frac{1}{2018}<0, Q(-1)=\frac{1}{a^2-2 a+2}+\frac{2017}{2018}>0 .
$$
Suy ra: $Q(-1) \cdot Q(0)<0$. Mặt khác $Q(x)$ là hàm số liên tục trên đoạn $[-1 ; 0]$ nên theo định lý Rolle, phương trình $Q(x)=0$ có nghiệm $x_1 \in(-1 ; 0)$.
Ta có: $Q(x)=\left(x-x_1\right) \cdot H(x)$, trong đó $H(x)$ là một đa thức có bậc 2017 là một số lê.
Chứng minh: $H(x)=0$ có ít nhất một nghiệm $x_2$.
Với $i=1 ; 2$, ta có: $Q\left(x_i\right)=0$, suy ra: $P\left(x_i\right)=x_i$. Do đó:
$$
P\left(P\left(x_i\right)\right)=P\left(x_i\right)=x_i .
$$
Vậy phương trình $P(P(x))=x$ có ít nhất 2 nghiệm là $x_1 ; x_2$.

Bài 6.4 (ĐH Kỹ thuật Hậu cần Công an Nhân dân). 
Đặt $P(x)=a\left(x-x_1\right)(x-$ $\left.x_2\right) \ldots\left(x-x_n\right), a \neq 0$. Ta có
$$
P^{\prime}(x)=P(x)\left[\frac{1}{x-x_1}+\frac{1}{x-x_2}+\cdots+\frac{1}{x-x_n}\right],\left(x \neq x_1, x_2, \ldots, x_n\right) .
$$
Theo định lý Rolle tổn tại $y_1, y_2, \ldots, y_{n-1}$
mà $x_1<y_1<x_2<y_2<\ldots<x_{n-1}<y_{n-1}<x_n$
để $P^{\prime}\left(y_1\right)=P^{\prime}\left(y_2\right)=\cdots=P^{\prime}\left(y_{n-1}\right)=0$.
Nhưng $P\left(y_i\right) \neq 0,(i=1,2, \ldots, n-1)$ nên
$$
\frac{1}{y_i-x_1}+\frac{1}{y_i-x_2}+\cdots+\frac{1}{y_i-x_n}=0,(i=1,2, \ldots, n-1),
$$suy ra
$$
\sum_{i=1}^{n-1}\left[\frac{1}{y_i-x_1}+\frac{1}{y_i-x_2}+\cdots+\frac{1}{y_i-x_n}\right]=0, \quad \text { hay } \quad \sum_{i=1}^{n-1} \sum_{k=1}^n \frac{1}{y_i-x_k}=0 .
$$
Ta lại có $P^{\prime}(x)=n a\left(x-y_1\right)\left(x-y_2\right) \ldots\left(x-y_{n-1}\right)$, nên
$$
P^{\prime \prime}(x)=P^{\prime}(x)\left[\frac{1}{x-y_1}+\frac{1}{x-y_2}+\cdots+\frac{1}{x-y_{n-1}}\right],\left(x \neq y_1, y_2, \ldots, y_{n-1}\right) .
$$
Do đó
$$
\sum_{k=1}^n \frac{P^{\prime}\left(x_k\right)}{P^{\prime}\left(x_k\right)}=\sum_{k=1}^n\left[\frac{1}{x_k-y_1}+\frac{1}{x_k-y_2}+\cdots+\frac{1}{x_k-y_{n-1}}\right]=\sum_{k=1}^n \sum_{i=1}^{n-1} \frac{1}{x_k-y_i}=0 .
$$

Bài 6.5 (HV Kỹ thuật Quân sự). 
- Không giảm tính tổng quát, giả sử
$$
a_n=1
$$
- Áp đụng định lý Viet ta có $\left(x_1+x_2+\ldots+x_n\right)^2=a_{n-1}^2=1, \sum_{i<j} x_i x_j=$
$$
a_{n-2}
$$
Do đó $0 \leq x_1^2+\ldots+x_n^2=\left(x_1+x_2+\ldots+x_n\right)^2-2 \sum_{i<j} x_i x_j=1-2 a_{n-2}$, nhận được $a_{n-2}=-1$ và $x_1^2+\ldots+x_n^2=3$.
- Từ $3=x_1^2+\ldots+x_n^2 \geq n \sqrt[5]{\left(x_1 \ldots x_n\right)^2}=n$, nhận được $n \leq 3$.
$$
\begin{aligned}
& -n=1, P(x)=x \pm 1 \\
& -n=2, P(x)= \pm\left(x^2 \pm x-1\right) \\
& -n=3, P(x)= \pm\left(x^3-x^2-x+1\right), P(x)= \pm\left(x^3+x^2-x-1\right)
\end{aligned}
$$

Bài 6.6 (ĐH Mỏ địa chất). 
Giả sử phương trình của đường thẳng là $y=a x+b$. Khi đó $x_i$ là nghiệm của phương trình
$$
2 x^4+7 x^3+(3-a) x-(5+b)=0 .
$$
Theo định lý Viet tổng các nghiệm bằng $-\frac{7}{2}$, và trung bình cộng của chúng bằng $-\frac{7}{8}$. Vậy đáp án là $-\frac{7}{8}$.

Bài 6.7 (ĐH Mỏ địa chất). 
Để ý là
$$
x^6=x^2+x
$$
Từ đó áp dụng định lý Viet có
$$
\sum x_i^5=\left(\sum x_i\right)^2-2 \sum x_i x_j+\sum x_i=0+0-0=0 .
$$
Bài 6.8 (ĐH Quy Nhơn). 
Viết $p(x)=a \prod_{i=1}^n\left(x-x_i\right), a \in \mathbb{R}$ và đặt
$$
p_k(x)=a \prod_{j \neq k}\left(x-x_j\right), \quad k=1, \ldots, n
$$
Khi đó $p^{\prime}(x)=\sum_{k=1}^n p_k(x)$ và $\left(x-x_k\right) p_k(x)=p(x)$ với mọi $k=1, \ldots, n$. Suy ra $p^{\prime}\left(x_j\right)=p_j\left(x_j\right)(\neq 0)$ vói mọi $j$.
Cuối cùng, xét đa thức
$$
F(x)=-1+\sum_{j=1}^n \frac{p_j(x)}{p^{\prime}\left(x_j\right)}
$$
có bậc $n-1$ vói hệ số cao nhất là $a\left(\frac{1}{p^{\prime}\left(x_1\right)}+\ldots \frac{1}{p^{\prime}\left(x_{\infty}\right)}\right)$. Hơn nữa ta có thể kiểm tra các $x_1, \ldots, x_n$ là nghiệm của $F(x)$ và do đó $F(x) \equiv 0$. Suy ra kết quả.

Bài 6.9 (ĐH Quy Nhơn). 
Viết $f(x)=\prod_{k=1}^n\left(b_k x+c_k\right)$ vói giả sử $b_k>0$ (do $a_n>0$ ) và $c_k>0$ (do đa thức có các hệ số không âm nên không thế có nghiệm dương) và có nhiều nhất một $c_k$ bằng 0 .
Tính
$$
f(1)=0+1+\ldots+n=\frac{n(n+1)}{2}=\prod_{k=1}^n\left(b_k+c_k\right) \geq 2^{n-1} .
$$
Suy ra $n \leq 4$. Do $f$ là không âm trên $\mathbb{R}$ nên nó có bậc chẵn, $n=2,4$.
Trường hợp $n=4$ không thể xảy ra vì $f(1)=10$ không thể viết thành tích của 4 nhân tử như vế phải đổng nhất thức trên đây.
Với $n=2$ : từ phân tích trên, $f$ chỉ có hai đang $f(x)=x(x+2)$ và $f(x)=$ $x(2 x+1)$. Cả hai dạng này đểu không thể không âm trên toàn bộ R .

Bài 6.10 (ĐH Sư phạm Hà Nội 2). 
Tứ giả thiết (1) suy ra nếu $x_0$ là một nghiệm thực của $P(x)$ thì ta có tất cả phẩn tử của đãy $\left\{x_n\right\}$ thỏa mãn: $x_n=$ $2 x_{n-1}^3+x_{n-1}, n=1,2,3, \ldots$ cúng là nghiệm của $P(x)$.
Hơn nữa, ta thấy nếu $x_0>0$ thì $x_0<x_1<x_2<\cdots x_n<x_{n+1} \cdots$ và nếu $x_0>0$ thì $x_0>x_1>x_2>\cdots x_n>x_{n+1} \cdots$
Do đó nếu $P(x)$ có một nghiệm thực khác 0 thì nó sẽ có vô số nghiệm thực phân biệt. Mà theo giả thiết $P(x)$ có bậc $n \geq 1$ dẫn đến mâu thuẫn. Vậy $P(x)$ không có nghiệm thực khác 0 .
Tiếp theo ta đi chứng minh $P(0) \neq 0$ với $P(x)=a_0 x^n+a_1 x^{n-1}+\cdots a_{n-1} x+$ $a_n, a_0 \neq 0$.
Thật vậy, giả sử $P(0)=0 \Leftrightarrow a_n=0$. Gọi $k$ là chỉ số lớn nhất thỏa mãn $a_k \neq 0$. Khi đó $P(x) \cdot P\left(2 x^2\right)=a_0^2 2^n \cdot x^{3 n}+\cdots+a_k^2 2^{n-k} \cdot x^{3(n-k)}$ và $P\left(2 x^3+x\right)=$ $a_0 2^n \cdot x^{3 n}+\cdots+a_k \cdot x^{n-k}$. Tứ $n-k>0 \Rightarrow 3(n-k)>n-k$ nên theo (1) đổng nhất hệ số ta có $a_k=0$ (mâu thuẫn). Vậy $P(x)$ không có nghiệm thực.

Bài 6.11 (ĐH Sư phạm Kỹ thuật Vīnh Long). 
Giả sử $P(x)=a_0+a_1 x+\ldots+$ $a_n x^n\left(a_i\right.$ nguyên, $\left.a_n \neq 0\right)$. Đặt
$$
Q(x)=P(x+1)=b_0+b_1 x+\ldots+b_n x^n \text { ( } b_i \text { nguyên). }
$$
Bồi vì $P\left(\frac{2017}{2019}\right)=0$ nên $Q\left(\frac{-2}{2019}\right)=P\left(\frac{2017}{2019}\right)=0$. Suy ra
$$
b_0+b_1\left(\frac{-2}{2019}\right)+\ldots+b_n\left(\frac{-2}{2019}\right)^n=0
$$
tương đương
$$
b_0 \cdot(2019)^n+b_1 \cdot(-2)(2019)^{n-1}+\ldots+b_n(-2)^n=0
$$

Từ đó suy ra $b_0$ là số chẵn. Mặt khác $b_0=Q(0)=P(1)=a_0+a_1+\ldots+a_n$. Vậy tống các hệ số của $P(x)$ không thể bằng 2019.

Bài 6.12 (ĐH Tây Bắc). 
(a) Ta có $f^{\prime}(x)=5 x^4-8 x$ có đúng 2 nghiệm thực là $x=0 ; x=\sqrt[3]{8 / 5}$ nên $f(x)$ có hai cực trị là
$$
f(0)=2>0 ; f(\sqrt[3]{8 / 5})=\frac{10-12 \sqrt[3]{64 / 25}}{5}<0
$$
Từ đó do tính liên tục của $f(x)$ suy ra $f(x)$ có đúng 3 nghiệm thực. Hơn nữa $f(-1)=-3 ; f(0)=2 ; f(1)=-1 ; f(2)=18$ nên 3 nghiệm thực của $f(x)$ tương ứng thuộc các khoảng $(-1,0) ;(0,1) ;(1,2)$.
Mặt khác ta có
$$
f(-2 x)=-32 x^5-16 x^2+2=-2\left(16 x^5+8 x^2-1\right)=-2 g(x)(*)
$$
Suy ra $g(x)$ cũng có đúng 3 nghiệm thực tương ứng thuộc các khoảng ( $-1,-1 / 2$ ); $(-1 / 2,0) ;(0,1 / 2)$.
Nếu gọi $b$ là nghiệm thực nhỏ nhất của $g(x)$ thì $b \in(-1,-1 / 2)$ và $g(b)=0$ suy ra $a=-2 b \in(1,2)$ hơn nữa từ đẳng thức (*) ta có $f(a)=f(-2 b)=$ $-2 g(b)=0$ vậy $a$ là nghiệm lớn nhất của $f(x)$ và $a+2 b=0$.
(b) Ta có:
$$
\begin{aligned}
\alpha^3 & =\left(\sqrt[3]{7+\sqrt{\frac{49}{8}}}+\sqrt[3]{7-\sqrt{\frac{49}{8}}}\right)^3 \\
& =14+3 \sqrt[3]{\left(7+\sqrt{\frac{49}{8}}\right)\left(7-\sqrt{\frac{49}{8}}\right)}\left(\sqrt[3]{7+\sqrt{\frac{49}{8}}}+\sqrt[3]{7-\sqrt{\frac{49}{8}}}\right) \\
& =14+\frac{21}{2} \alpha
\end{aligned}
$$
Suy ra $\alpha$ là nghiệm của đa thức $g(x)=2 x^3-21 x-28$.
Chia đa thức $2 x^5-2 x^4-23 x^3-7 x^2+49 x+30$ cho $g(x)$ ta được:
$$
2 x^5-2 x^4-23 x^3-7 x^2+49 x+30=g(x)\left(x^2-x-1\right)+2 .
$$
Suy ra $f(\alpha)=2^5=32$.