Bài 7.1 (ĐH Giao thông Vận tải).
Ứng với một cách cắt ta đánh số các đoạn từ 1 đến 351 . Ký hiệu số thứ tự của các đoạn 10 m là $a_1, a_2, \ldots, a_{10}$, số thứ tự của đoạn 18 m là $a$. Để thực hiện một cách cắt theo đúng yêu cầu ta thực hiện theo các bước.
Bước 1: chọn giá trị của $a$ trong tập $\{1,2, \ldots, 351\}$.
Bước 2: chọn một tập con $\left\{a_1, a_2, \ldots, a_{100}\right\}$ của 350 số còn lại.
Bước 3: cất cuộn đẩy theo thứ tự đã chọn. Như vậy số cách cắt cuộn đây là $n=351 C_{350}^{100}$.

Bài 7.2 (ĐH Kiến Trúc Hà Nội). 
50 viên bi được chia làm ba loại gồm: 16 viên bi có số chia hết cho 3 ; 17 viên bi có số chia 3 dư 1 và 17 viên bi còn lại có số chia 3 dư 2 .
Có hai trường hợp xảy ra:
- 3 viên bi được chọn cùng một loại, trong trường hợp này có: $C_{16}^3+C_{17}^3+$ $C_{17}^6=1920$ (cách).
- 3 viên bi được chọn thuộc ba loại khác nhau, trong trường hợp này có: $C_{16}^1 \cdot C_{17}^1 \cdot C_{17}^1=4624$ (cách).
Vậy có tất cả: $1920+4624=6544$ (cách).

Bài 7.3 (ĐH Kiến Trúc Hà Nội). 
Gọi $a_n$ là cách sấp xếp giỏ trái cây thỏa mãn để bài và $F(x)$ là hàm sinh của đây $a_n$. Ta có
$$
F(x)=\sum_{n=0}^{+\infty} a_n \cdot x^n=f(x) \cdot g(x) \cdot h(x) \cdot k(x)
$$
trong đó $f(x), g(x), h(x), k(x)$ tương ứng là hàm sinh cho số cách chọn các loại quả lê, quả chuối, quả ổi, quả bưởi.
Ta có: hàm sinh cho số cách chọn quả lê là:
$$
f(x)=1+x^2+x^4+\cdots=\frac{1}{1-x^2}
$$
Hàm sinh cho số cách chọn quả chuối là:
$$
g(x)=1+x^6+x^{12}+\cdots=\frac{1}{1-x^6}
$$
Hàm sinh cho số cách chọn quả ổi là:
$$
h(x)=1+x+x^2+x^3+x^4+x^5=\frac{1-x^6}{1-x}
$$
Hàm sinh cho số cách chọn quả bưởi là:
$$
k(x)=1+x
$$
Do đó:
$$
F(x)=\frac{1}{1-x^2} \cdot \frac{1}{1-x^6} \cdot \frac{1-x^5}{1-x} \cdot(1+x)=\frac{1}{(1-x)^2}=\sum_{k=0}^{+\infty}(k+1) \cdot x^k
$$
Đẳng thức cuối cùng nhận được bằng cách lấy đạo hàm hai vế đẳng thức
$$
\frac{1}{1-x}=\sum_{k=0}^{+\infty} x^k
$$
Suy ra $a_n=n+1$. Vậy số cách sấp xếp giỏ trái cây thỏa mãn đề bài là $n+1$.

Bài 7.5 (ĐH Kiến Trúc Hà Nội). 
Ta chỉ cần chứng tỏ tồn tại một khối cầu có bán kính là 1 chứa ít nhất 22 điểm của tập $A$.
Gọi $\left(S_1\right)$ là khối cầu có tâm là điểm $A_1$, bán kính $R=1$ (kể cả biên).
Nếu tất cả các điểm $A_i(i=2 ; 3 ; \cdots ; 64)$ đểu thuộc $\left(S_1\right)$ thì ta có ngay điều phải chứng minh.
Xét trường hợp tổn tại điểm của tập hợp $\left\{A_2 ; A_3 ; \cdots ; A_{64}\right\}$ không thuộc khối cẩu $\left(S_1\right)$, không mất tính tổng quát ta có thể giả sử điểm đó là $A_2$. Ta có
$$
A_1 A_2>1
$$
Gọi $\left(S_2\right)$ là khối cầu có tâm là điểm $A_2$ và có bán kính bằng 1 (kể cả biên). Nếu tất cả các điểm $A_i(i=3 ; 4 ; \cdots ; 64)$ đểu thuộc khối cẩu $\left(S_1\right)$ hoặc khối cầu $\left(S_2\right)$ thì theo nguyên lý Dirichle, tồn tại một trong hai khối cẩu $\left(S_1\right)$ hoặc $\left(S_2\right)$ chứa ít nhất 31 điểm của tập $A$. Từ đó ta thu được điều phải chứng minh. Xét trường hợp tổn tại điểm của tập hợp $\left\{A_3 ; A_4 ; \cdots ; A_{64}\right\}$ không thuộc cả hai khối cẩu $\left(S_1\right) ;\left(S_2\right)$. Không mất tính tổng quát ta có thế giả sử điểm đó là $A_3$. Khi đó hiển nhiên ta có:
$$
A_3 A_1>1 ; A_3 A_2>1
$$
Gọi $\left(S_3\right)$ là khối cầu có tâm là điểm $A_3$ và có bán kính bằng 1 (kể cả biên). Với bất kì $i=4 ; 5 ; \cdots ; 64$, xét 4 điểm $A_1 ; A_2 ; A_3 ; A_i$. Theo giả thiết tồn tại 2 điểm trong 4 điểm đó có khoảng cách không vượt quá 1. Mặt khác đo $A_1 A_2 ; A_1 A_3 ; A_2 A_3>1$ nên ta suy ra: hoặc $A_i A_1 \leq 1$, hoặc $A_i A_2 \leq 1$, hoặc $A_i A_3 \leq 1$. Nghĩa là bất kỳ các điểm $A_4 ; A_5 ; \cdots ; A_{64}$ đều thuộc ít nhất một trong ba khối cầu $\left(S_1\right) ;\left(S_2\right) ;\left(S_3\right)$. Theo nguyên lý Dirichle, tồn tại một trong ba khối cầu $\left(S_1\right),\left(S_2\right),\left(S_3\right)$ chứa ít nhất 21 điểm của tập $\left\{A_4 ; A_5 ; \cdots ; A_{64}\right\}$, và do đó khối cầu này sẽ chứa ít nhất 22 điếm (bao gồm cả tâm của khối cẩu đó) của tập $A$.