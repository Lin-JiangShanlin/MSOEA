import MSOEA_f as MSOEA



test_list = ["3SBP1"]
read_list = ["3S"]

storepath = 'Data/'


for t in range(0, 1):
	MSOEA.exe_main(test_list, read_list, t, storepath)
	print("{}th test done!".format(t))
	print("\n")