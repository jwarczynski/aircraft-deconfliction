1. first constraint
   - $$
     \forall_i\sum_{j=1}^{7}x_{ij} = 1  
     $$
   - each plane can choose only one maneuver   
<br>
2. second constraint
   - $$
     \sum_{i=1}^{10}\sum_{j=1}^{7}\sum_{k=1}^{10}\sum_{l=1}^{7}x_{ij}x_{kl}c_{ijkl} = 0
     $$
   - above not linear, but can be written as  follows:
   - $$
     \forall_i\forall_j\forall_k\sum_{l=1}^{7}(x_{ij}c_{ijkl} + x_{kl}c_{ijkl}) \leq 1 \
     $$
   - there could not be collsion 
