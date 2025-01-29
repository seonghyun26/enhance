for i in {0..3}; do
    gmx grompp -f nvt.mdp -c A.gro -p topol.top -o nvt/$i.tpr
    sleep 1
done