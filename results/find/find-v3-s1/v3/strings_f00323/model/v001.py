def predict(probe):
    # Reverses the entire string [E1]
    # Evidence: "apple"->"elppa", "test case "->"esactset" (trailing space dropped? no—reversed " esac tset" = "test case " reversed is " esac tset"... let's check)
    # "test case " reversed = " esac tset" but observed "esactset" (no leading space, no trailing space)
    # Actually "test case " = t,e,s,t,space,c,a,s,e,space -> reversed = space,e,s,a,c,space,t,s,e,t = " esac tset"
    # Observed "esactset" = e,s,a,c,t,s,e,t. So spaces are removed AND reversed.
    # "test caseMiXeD" reversed = "DeXiMesac tset" -> observed "DeXiMesactset" (space removed)
    # "data a Python " reversed = " nohtyP a atad" -> observed "nohtyPaatad" (spaces removed)
    # "Mississippi Hello World data" reversed = "atad dlroW olleH ippississiM" -> observed "ataddlroWolleHippississiM" (spaces removed)
    # So: remove all spaces, then reverse.
    return {"outputs": [s.replace(" ", "")[::-1] for s in probe["inputs"]]}
