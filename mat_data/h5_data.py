import h5py
import numpy as np
f=h5py.File("myh5py.hdf5","w")
    
for key in f.keys():
    print(key)
    print(f[key].name)
    print(f[key].shape)
    print(f[key].value)
d1=f.create_dataset("dset1", (20,), 'i')
d1[...]=np.arange(20)
f["dset2"]=np.arange(15)
d1=f.create_dataset("dset1",data=a)
g1=f.create_group("bar1")
c1=g1.create_group("car1")
d1=g1.create_dataset("dset1",data=np.arange(10))
print(c1.keys())
