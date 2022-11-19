from operator import indexOf
import os
import uuid
import re
import time

# Auxiliary functions
from parsing import *
from utils import *
from structs import *
from models import *
from controllers import *

def main():
    MIGRATIONS_PATH = input("Paste the path to your (clean) migrations file:\n")


    # Letting user create package name
    pkg_name_qst = "\nPlease enter the main package name (must be lowercase):\n\n"
    pkg_name_error_msg = "Invalid package name."
    pkg_name_confirm_msg = "\nIs this correct? (Y/N)\n\n"
    MAIN_PACKAGE_NAME = validateInput_PkgName(pkg_name_qst, pkg_name_error_msg, pkg_name_confirm_msg)

    print("Looking for file...")
    with open(f"{MIGRATIONS_PATH}", 'r') as file:
        data = file.read()
    print("Found file")
    tablesOut = getTablesFromSQLFile(data)
    print("Successfully parsed tables")

    tableGroups = []
    tables_in_tableGroup = {}
    table_objs_in_tableGroup = {}

    # Begin iterating over per table
    for table in tablesOut:

        if len(tableGroups) == 0:
            print(f"\nCURRENTLY HANDLING TABLE {table['name']} ({indexOf(tablesOut, table) + 1} / {len(tablesOut)})")
            sub_pkg_name_qst = "\nPlease enter the new sub-package name (lowercase only):\n\n"
            sub_pkg_name_error_msg = "Invalid package name."
            sub_pkg_name_confirm_msg = "\nIs this correct? (Y/N):\n\n"
            SUB_PACKAGE_NAME = validateInput_PkgName(sub_pkg_name_qst, sub_pkg_name_error_msg, sub_pkg_name_confirm_msg)
            tableGroups.append(SUB_PACKAGE_NAME)
            tables_in_tableGroup[SUB_PACKAGE_NAME] = [table['name']]
            table_objs_in_tableGroup[SUB_PACKAGE_NAME] = {}
            table_objs_in_tableGroup[SUB_PACKAGE_NAME][table['name']] = table
        else:
            print("\nYou have the following subgroups:\n--------------------------------------")

            for subgroup_idx in range(len(tableGroups)):
                print(f"\t({subgroup_idx + 1}):\t{tableGroups[subgroup_idx]} - ({tables_in_tableGroup[tableGroups[subgroup_idx]]})")

            print("--------------------------------------\n")
            print(f"\nCURRENTLY HANDLING TABLE {table['name']} ({indexOf(tablesOut, table) + 1} / {len(tablesOut)})")
            # New or existing subgroup
            want_new_group = False
            answers = {
                "Y" : True,
                "y" : True,
                "N" : False,
                "n" : False,
                "no" : False,
                "yes" : True
            }
            ask_new_group = validateInput_Dict(qst = f"\nDo you want to create a new group for table {table['name']}? (Y/N)\n\n", allowed = answers, error_msg = "Invalid input - try again.")

            # Creating a new subgroup
            if ask_new_group == True:
                sub_pkg_name_qst = "\nPlease enter the new sub-package name (lowercase only):\n\n"
                sub_pkg_name_error_msg = "Invalid package name."
                sub_pkg_name_confirm_msg = "\nIs this correct? (Y/N)\n\n"
                SUB_PACKAGE_NAME = validateInput_PkgName(sub_pkg_name_qst, sub_pkg_name_error_msg, sub_pkg_name_confirm_msg)
                tableGroups.append(SUB_PACKAGE_NAME)
                tables_in_tableGroup[SUB_PACKAGE_NAME] = [table['name']]
                table_objs_in_tableGroup[SUB_PACKAGE_NAME] = {}
                table_objs_in_tableGroup[SUB_PACKAGE_NAME][table['name']] = table

            # Linking to an existing subgroup
            else:
                link_qst = f"\nEnter the value of the subgroup you want to link the table to (1 - {len(tableGroups)}): \n\n"
                error_msg = "Could not link the table to group - try again."

                SUB_PACKAGE_NAME = validateInput_subGroupName(link_qst, error_msg, tableGroups)
                tables_in_tableGroup[SUB_PACKAGE_NAME].append(table['name'])
                table_objs_in_tableGroup[SUB_PACKAGE_NAME][table['name']] = table

        # TABLE HAS NOW BEEN CATEGORIZED AND LINKED PROPERLY
        print(f"Table {table['name']} has been successfully read and put in subgroup {SUB_PACKAGE_NAME}")

    print(f"{len(tableGroups)} tables have been categorized properly")
    for tableGroup in tableGroups:
        print(f"{indexOf(tableGroups, tableGroup) +1}.\t{tableGroup}")

    # Now iterating over each group to create a controller file

    for tableGroup in tableGroups:

        # Generating controller file
        controller_file = f"package {MAIN_PACKAGE_NAME}" + "\n\n"

        for table in tables_in_tableGroup[tableGroup]:

            table_obj = table_objs_in_tableGroup[tableGroup][table]

            controller_file += createControllerFile(
                table_obj,
                MAIN_PACKAGE_NAME,
                "auth"
            )


        # Create a new directory because it does not exist
        isExist = os.path.exists(f"{MAIN_PACKAGE_NAME}")
        if not isExist:
            os.makedirs(MAIN_PACKAGE_NAME)
            print("The new directory is created!")


        output_file = open(f"{MAIN_PACKAGE_NAME}/{tableGroup}.controllers.go", "a")
        output_file.write(controller_file)
        output_file.close()
    
    for tableGroup in tableGroups:

        # Generating controller file
        models_file = f"package models" + "\n\n"

        for table in tables_in_tableGroup[tableGroup]:

            table_obj = table_objs_in_tableGroup[tableGroup][table]

            models_file += createModelsFile(table_obj)


        # Create a new directory because it does not exist
        isExist = os.path.exists(f"{MAIN_PACKAGE_NAME}/models/")
        if not isExist:
            os.makedirs(f"{MAIN_PACKAGE_NAME}/models/")
            print("The new directory is created!")


        output_file = open(f"{MAIN_PACKAGE_NAME}/models/{tableGroup}.go", "a")
        output_file.write(models_file)
        output_file.close()
        

if __name__ == '__main__':
    main()