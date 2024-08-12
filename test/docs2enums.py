if __name__ == '__main__':
    # EXAMPLE
    def convert_api_description_to_enums():
        import re

        api_description = """
        General
        Edit ACL propagated items	0x400	1024
        Units and unit groups
        View routes	0x4000000	67108864
        Create, edit, delete routes	0x8000000	134217728
        View events	0x1000000000	68719476736
        Create, edit, and delete events	0x2000000000	137438953472
        Use unit in jobs, notifications, routes, retranslators	0x8000000000	549755813888
        Resources (Accounts)
        Manage account	0x100000000	4294967296
        """

        # pattern = r"(0x[0-9a-f]+)\s+(\d+)\s+(.+)"

        # for i in re.findall(pattern, api_description):
        #     eid, intvalue, desc = i
        #     print(f"\t{desc.upper().replace(' ', '_')} = {eid}  # {intvalue}, {desc}")

        # pattern = r"(0x[0-9a-f]+)\s+(.+)"
        #
        # for i in re.findall(pattern, api_description):
        #     eid, desc = i
        #     print(f"\t{desc.upper().replace(' ', '_')} = {eid}  # {desc}")

        pattern = r"(.+)\s+(0x[0-9a-f]+)\s+(\d+)"

        for i in re.findall(pattern, api_description):
            desc, eid, decval = i
            print(f"\t{desc.upper().replace(' ', '_')} = {decval}  # {eid}, {desc}")


    convert_api_description_to_enums()
