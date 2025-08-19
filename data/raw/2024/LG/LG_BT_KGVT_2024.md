Bài 4.1 (ĐH Giao thông Vận tải).
(a) Do $M \neq N$ và $N \subset(M+N)$ nên $M \neq(M+N)$. Kết hợp $M \subset(M+N)$ và $M \neq(M+N)$ ta suy ra $\operatorname{dim}(M+N)>\operatorname{dim} M=2023$. Mặt khác $(M+$ $N) \subset \mathbb{R}^{2024}$ nên $\operatorname{dim}(M+N) \leqslant 2024$. Kết hợp các phân tích này ta suy ra $\operatorname{dim}(M+N)=2024$. Sử dụng đẳng thức
$$
\operatorname{dim} M+\operatorname{dim} N=\operatorname{dim}(M+N)+\operatorname{dim}(M \cap N)
$$
ta suy ra $\operatorname{dim}(M \cap N)=2022$.
(b) Ta cần chỉ ra $(M \cap N) \not \subset P$. Thực vậy, nếu $(M \cap N) \subset P$ thì kết hợp với $(M \cap N) \subset N$ ta suy ra $(M \cap N) \subset(N \cap P)$. Theo câu a, $(M \cap N)$ là một không gian con 2022 chiều của $\mathbb{R}^{2024}$ và chứng minh tương tự ta cũng có $(N \cap P)$ là một không gian con 2022 chiều của $\mathbb{R}^{2024}$. Như vậy từ bao hàm thức $(M \cap N) \subset(N \cap P)$ ta suy ra $(M \cap N)=(N \cap P)$ nhưng điều này lại trái với giả thiết. Như vậy, ta phải có $(M \cap N) \not \subset P$ như đã nhắc đến ở trên.
Sử dụng $(M \cap N) \not \subset P$ và phân tích tương tự như câu a, ta suy ra được $\operatorname{dim}((M \cap N)+P)=2024$. Như vậy từ đẳng thức
$$
\operatorname{dim}(M \cap N)+\operatorname{dim} P=\operatorname{dim}((M \cap N)+P)+\operatorname{dim}(M \cap N \cap P)
$$
ta thu được $\operatorname{dim}(M \cap N \cap P)=2021$.

Bài 4.2 (ĐH Mỏ-Địa chất). Đặt các véc tơ có gốc tại tâm $O$. Nếu các điểm cuối của các véc tơ không tạo thành một tam giác nhọn thì tất cả các mút (điểm cuối của véc tơ) này đều nằm trên nửa đường tròn tâm $O$ bán kính bằng 1. Lấy đối xứng một véc tơ (giả sử lấy véc tơ ở giữa). Khi đó các điểm cuối của hai véc tơ cũ và điểm cuối của véc tơ đối xứng ảnh tạo thành một tam giác nhọn. Giả sử các véc tơ mới là $(x, y, z)$. Trong đó có hai véc tơ cũ từ bộ $(u, w, z)$ - các véc tơ này lấy dấu dương, và một véc tơ lấy đối xứng - véc tơ này lấy dấu âm. Giả sử $h=x+y+z$. Ta đi tìm các tích vô hướng của các cặp véc tơ sau:
$$
\begin{gathered}
<h-x, y-z>=<y+z, y-z>=|y|^2-|z|^2=0 \\
<h-y, x-z>=<x+z, x-z>=|x|^2-|z|^2=0 \\
<h-z, y-x>=<y+x, y-x>=|y|^2-|x|^2=0
\end{gathered}
$$
Điều đó có nghĩa $h$ chính là véc tơ có gốc ở gốc tọa độ và đỉnh chính là giao điểm của ba đường cao của tam giác, tức là $h$ nằm trong đường tròn đơn vị với bán kính bằng 1 . Đây chính là điều phải chứng minh.

Bài 4.3 (ĐH Hải Phòng).
(a) Với $\lambda=0$, ta có
$$
\varphi(p(x))=x(x+1) p^{\prime}(x)-2 x p(x)
$$
Xét đa thức $p(x)=a x^2+b x+c \in \operatorname{Ker}(\varphi)$, ta có $\varphi(p(x))=0$ hay
$$
x(x+1)(2 a x+b)-2 x\left(a x^2+b x+c\right)=0 \Leftrightarrow(2 a-b) x^2+(b-2 c) x=0 .
$$
Suy ra
$$
\left\{\begin{array} { l } 
{ 2 a - b = 0 } \\
{ b - 2 c = 0 }
\end{array} \Leftrightarrow \left\{\begin{array}{l}
b=2 a \\
c=a
\end{array}\right.\right.
$$
Vậy $p(x)=a\left(x^2+2 x+1\right)$. Ta có $\left\{x^2+2 x+1\right\}$ là một cơ sở của $\operatorname{Ker} \varphi$ và $\operatorname{dimKer} \varphi=1$.
Xét đa thức $q(x)=\varphi(p(x)) \in \operatorname{Ker} \varphi$, ta có
$$
q(x)=2 a x^2+b\left(-x^2+x\right)-2 c x
$$
Vậy $\left\{x^2,-x^2+x, x\right\}$ là một hệ sinh của $\operatorname{Im} \varphi$. Dễ thấy $\left\{x^2, x\right\}$ là một cơ sở của $\operatorname{Im} \varphi$, do đó $\operatorname{dim} \operatorname{Im} \varphi=2$.
(b) Xét đa thức $p(x)=a x^2+b x+c \in \operatorname{Ker}(\varphi)$, suy ra $\varphi(p(x))=0$ hay
$$
q(x)=[2(1-\lambda) a-b] x^2+[-2 \lambda a+(1-\lambda) b-2 c] x-\lambda b=0
$$
với mọi $x \in \mathbb{R}$. Suy ra
$$
\left\{\begin{array}{l}
2(1-\lambda) a-b=0 \\
(1-\lambda) b-2 \lambda a-2 c=0 \\
\lambda b=0
\end{array}\right.
$$
Vì $\varphi$ là tự đồng cấu của không gian véctơ hữu hạn chiều nên nó đẳng cấu khi và chỉ khi nó là đơn cấu, nghĩa là $\operatorname{Ker} \varphi=0$. Điều đó có nghĩa là hệ phương trình trên chỉ có nghiệm tầm thường $a=b=c=0$, hay định thức của ma trận hệ số khác 0 :
$$
\left|\begin{array}{ccc}
2(1-\lambda) & -1 & 0 \\
-2 \lambda & 1-\lambda & -2 \\
0 & \lambda & 0
\end{array}\right| \neq 0 \Leftrightarrow-4 \lambda^2+4 \lambda \neq 0 \Leftrightarrow \lambda \neq 0,1
$$

Bài 4.4 (ĐH Trà Vinh).
(a) Ký hiệu $W$ là tập đang xét. Rõ ràng $0 \in W$ nên $W \neq \emptyset$. Với $f, g \in W$ ta có
$$
\begin{aligned}
(f+g)^{\prime}+4(f+g) & =\left(f^{\prime}+4 f\right)+\left(g^{\prime}+4 g\right)=0 \\
(\alpha f)^{\prime}+4(\alpha f) & =\alpha\left(f^{\prime}+4 f\right)=0
\end{aligned}
$$
Do đó $f+g, \alpha f \in W$. Vậy $W$ là một không gian véctơ con của $W$.
(b) Nghiệm tổng quát của phương trình vi phân $f^{\prime}+4 f=0$ là
$$
f(x)=c e^{-4 x}, \quad c \in \mathbb{R}
$$
Do đó $\left\{e^{-4 x}\right\}$ là một cơ sở của $W$ và $\operatorname{dim} W=1$.