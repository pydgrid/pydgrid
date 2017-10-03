import subprocess
import os



from_dir = os.path.join('.','svg')
to_dir = os.path.join('.','png')

for filenameExtension in os.listdir(from_dir):
    print(filenameExtension)
    filename, ext=os.path.splitext(filenameExtension)
    p=subprocess.call(['/usr/bin/inkscape', from_dir + '/' + filename + '.svg', '--export-dpi=300', '--export-png',to_dir + '/' + filename + '.png'])

