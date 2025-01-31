bash md.sh aldp AE 1 &
bash md.sh aldp AE 10
wait

bash md.sh aldp AE 250 &
bash md.sh aldp TAE 1
wait

bash md.sh aldp TAE 10 &
bash md.sh aldp TAE 250
wait

bash md.sh aldp VDE 1 &
bash md.sh aldp VDE 10 
wait

bash md.sh aldp VDE 250 &
bash md.sh aldp DeepLDA 1
wait

bash md.sh aldp DeepLDA 10 &
bash md.sh aldp DeepLDA 250 
wait

bash md.sh aldp DeepTDA 1 &
bash md.sh aldp DeepTDA 10
wait

bash md.sh aldp DeepTDA 250 &
bash md.sh aldp DeepTICA 1
wait

bash md.sh aldp DeepTICA 10 &
bash md.sh aldp DeepTICA 250