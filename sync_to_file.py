def sync_to_file(adult, child,age_list,passenger_discount,user_dic):
    with open("write_adult_file.txt", 'w+') as hFile:
        hFile.write("Adult_Fare\n")
        for i in range(len(adult)):
            for j in range(len(adult)):
                hFile.write("%s:" % adult[i][j])
            hFile.write("\n")
        hFile.write("Age\n")
        hFile.write("%s %s\n%s %s" % (age_list[0], age_list[1], age_list[2], age_list[3]))

    with open("write_child_file.txt", 'w+') as hFile:
        hFile.write("Child_Fare\n")
        for i in range(len(child)):
            for j in range(len(child)):
                hFile.write("%s:" % child[i][j])
            hFile.write("\n")
        hFile.write("Passenger_Discount\n")
        for i in range(len(passenger_discount)):
            for j in range(len(passenger_discount)):
                hFile.write("%s." % passenger_discount[i][j])
            hFile.write("\n")

    with open("user_info.txt", 'w+') as hFile:
        hFile.write("User Travel Information\n")
        for key,value in user_dic.items():
            for sub_key,sub_value in value.items():
                hFile.write("%s %s %s %s\n" % (key,sub_key[0],sub_key[1],sub_value))
    return adult, child
