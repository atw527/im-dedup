import commands
import os
import os.path
import re
import shutil

os.chdir("/usr/local/data")

frames = sorted(os.listdir("inbox"))
frame_count = len(frames)

commands.getstatusoutput("rm -f outbox/*.jpg")
commands.getstatusoutput("rm -f outbox/*.JPG")

# remove sequential duplicates

x = 0
y = 1
exceptions = 0
while True:
    try:
        if x > frame_count - 1 or y > frame_count:
            break

        filename, file_extension = os.path.splitext("inbox/{0}".format(frames[x]))
        if file_extension.upper() != ".JPG":
            print file_extension
            x += 1
            y = x + 1
            continue

        filename, file_extension = os.path.splitext("inbox/{0}".format(frames[y]))
        if file_extension.upper() != ".JPG":
            print file_extension
            y += 1
            continue

        cmd = "compare -metric RMSE inbox/{0} inbox/{1} NULL: 2>&1".format(frames[x], frames[y])
        print cmd
        (return_val, output) = commands.getstatusoutput(cmd)
        diff = int(re.search('[0-9]+', output).group())

        print diff

        if diff < 5000 and diff != 0:
            y += 1
        else:
            shutil.copy2("inbox/"+frames[x], "outbox/")
            # frame has changed, set this as the new starting point
            x = y
            y = x + 1

    except Exception, e:
        print str(e)
        # reset the frame indexes to try to get out of this exception
        x = y
        y += 1
        exceptions += 1
        continue

print "Exceptions: " + str(exceptions)


# remove non-sequential duplicates

frames = sorted(os.listdir("outbox"))
frame_count = len(frames)

x = 0
y = 1
exceptions = 0
while True:
    try:
        if y > frame_count:
            # find which files are left
            frames = sorted(os.listdir("outbox"))
            frame_count = len(frames)
            x += 1
            y = x

        if x > frame_count + 1:
            break

        filename, file_extension = os.path.splitext("outbox/{0}".format(frames[x]))
        if file_extension.upper() != ".JPG":
            print file_extension
            x += 1
            y = x + 1
            continue

        filename, file_extension = os.path.splitext("outbox/{0}".format(frames[y]))
        if file_extension.upper() != ".JPG":
            print file_extension
            y += 1
            continue

        cmd = "compare -metric RMSE outbox/{0} outbox/{1} NULL: 2>&1".format(frames[x], frames[y])
        print cmd
        (return_val, output) = commands.getstatusoutput(cmd)
        diff = int(re.search('[0-9]+', output).group())

        print diff

        if diff < 5000 and diff != 0:
            os.remove("outbox/{0}".format(frames[y]))
            y += 1
        else:
            # frame has changed, set this as the new starting point
            y += 1

    except Exception, e:
        print str(e)
        # reset the frame indexes to try to get out of this exception
        y += 1
        exceptions += 1
        continue

print "Exceptions: " + str(exceptions)
