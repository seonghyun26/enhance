for i in {0..7}; do
    gmx grompp -f nvt.mdp -c A.gro -p topol.top -o nvt_600K/$i.tpr
    sleep 1
done