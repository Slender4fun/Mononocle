import os, device, display, gc
bdev = device.Storage()
os.VfsLfs2.mkfs(bdev)
display.show(display.Text("Monocle is now Empty",0,0,display.RED))
gc.collect()
print(os.listdir())