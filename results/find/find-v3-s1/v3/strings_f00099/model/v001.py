def predict(probe):
    # The box reverses each input string [E1]
    # Evidence: "apple"->"elppa", "test case "->"esac tset",
    # "test caseMiXeD"->"DeXiMesac tset", "data a Python "->"nohtyP a atad",
    # "test case Zebra"->"arbeZ esac tset",
    # "Mississippi Hello World data"->"atad dlroW olleH ippississiM"
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
