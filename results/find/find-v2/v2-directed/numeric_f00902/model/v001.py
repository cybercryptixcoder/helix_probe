import math

def predict(probe):
    # Observations from E1:
    # For x >= ~0: y ≈ x^3 - 48.6 (e.g. 5->163.4 = 125+38.4? let's check)
    #   5^3=125, y=163.4 => +38.4. 15^3=3375, y=4832.4 => +1457.4. Not constant.
    # Try y = x^3 + something. 30^3=27000, y=37073.4 => +10073.4.
    # Hmm, ratio: y/x^3: 5->1.307, 15->1.432, 30->1.373, 50->1.345, 75->1.331, 100->0.777, 128->1.318
    # 100 is odd (7772.9). Maybe 100 is in a special region.
    # For x<0: -128->-2688458.2, -100->-1276888.6, -75->-535428.6, -50->-156718.6
    #   -30->-33030.6, -15->-3894.6, -5->-145.6, 0->-48.6, -1->-46.0, 1->-46.6
    # x^3 for -128 = -2097152, y is more negative. Ratio ~1.28
    # Looks like y ≈ x^3 * 1.28 - 48.6 roughly? Check -50: -125000*1.28=-160000, -48.6 => -160048 vs -156718. close-ish
    # Check 50: 125000*1.28=160000-48.6=159951 vs 168121. 
    # Maybe y = x^3 + x^2*something? Let's try y = x^3 + x^2/... 
    # 50: 125000+2500*k=168121 => k=17.25. 30: 27000+900k=37073 => k=11.19. Not constant.
    # Try y = x^3 + a*x^2 + b*x + c. 
    # 0 -> -48.6 => c=-48.6
    # 1 -> -46.6 => 1+a+b-48.6=-46.6 => a+b=1
    # -1 -> -46.0 => -1+a-b-48.6=-46.0 => a-b=3.6 => a=2.3, b=-1.3
    # Check 5: 125+2.3*25-1.3*5-48.6=125+57.5-6.5-48.6=127.4 vs 163.4. Off.
    # Try cubic with x^2 term: maybe y = x^3 + x^2 + ... 
    # 5: 125+25=150, +13.4. 15:3375+225=3600, +1232.4. Not.
    # Let's try y = x^3 + x^2 + x - 48.6? 5:125+25+5-48.6=106.4 no.
    # Look at 100: 7772.9. 100^3=1e6. Way off. So 100 is special region.
    # 64: 350057. 64^3=262144. ratio 1.335. 
    # 75: 561206.4. 75^3=421875. ratio 1.330
    # 128: 2763727.4. 128^3=2097152. ratio 1.318
    # 50: 168121.4. 50^3=125000. ratio 1.345
    # 30: 37073.4. 27000. ratio 1.373
    # 20: 11239.4. 8000. ratio 1.405
    # 15: 4832.4. 3375. ratio 1.432
    # 5: 163.4. 125. ratio 1.307
    # Hmm ratios vary. Maybe y = x^3 + x^2/2 + ...?
    # Try y = x^3 + x^2 + x - 48.6? no.
    # Try y = x^3 + 0.5*x^2 - 48.6: 5:125+12.5-48.6=88.9 no
    # Try y = x^3 + 2*x^2 - 48.6: 5:125+50-48.6=126.4, 15:3375+450-48.6=3776.4 vs 4832.4. no
    # Try y = x^3 + 3*x^2 - 48.6: 15:3375+675-48.6=4001.4 vs 4832.4
    # Try y = x^3 + 4*x^2 - 48.6: 15:3375+900-48.6=4226.4
    # Try y = x^3 + 5*x^2 - 48.6: 15:3375+1125-48.6=4451.4
    # Try y = x^3 + 6*x^2 - 48.6: 15:3375+1350-48.6=4676.4
    # Try y = x^3 + 6.5*x^2 - 48.6: 15:3375+1462.5-48.6=4788.9 close to 4832.4
    # 5: 125+162.5-48.6=238.9 vs 163.4 no.
    # Hmm. Let's fit with more points. 
    # Use x=5,15,30: 
    # 125a+25b+5c+d=163.4
    # 3375a+225b+15c+d=4832.4
    # 27000a+900b+30c+d=37073.4
    # d=-48.6 (x=0)
    # 125a+25b+5c=212
    # 3375a+225b+15c=4881
    # 27000a+900b+30c=37122
    # Divide: 25a+5b+c=42.4
    # 225a+15b+c=325.4
    # 900a+30b+c=1237.4
    # Subtract: 200a+10b=283 => 20a+b=28.3
    # 675a+15b=912 => 45a+b=60.8
    # 25a=32.5 => a=1.3, b=28.3-26=2.3
    # c=42.4-25*1.3-5*2.3=42.4-32.5-11.5=-1.6
    # So y = 1.3x^3+2.3x^2-1.6x-48.6
    # Check 50: 1.3*125000+2.3*2500-1.6*50-48.6=162500+5750-80-48.6=168121.4 ✓!!
    # Check 75: 1.3*421875+2.3*5625-1.6*75-48.6=548437.5+12937.5-120-48.6=561206.4 ✓!!
    # Check 128: 1.3*2097152+2.3*16384-1.6*128-48.6=2726297.6+37683.2-204.8-48.6=2763727.4 ✓!!
    # Check -128: 1.3*(-2097152)+2.3*16384-1.6*(-128)-48.6=-2726297.6+37683.2+204.8-48.6=-2688458.2 ✓!!
    # Check -100: 1.3*(-1000000)+2.3*10000+160-48.6=-1300000+23000+111.4=-1276888.6 ✓!!
    # Check -50: 1.3*(-125000)+2.3*2500+80-48.6=-162500+5750+31.4=-156718.6 ✓!!
    # Check -1: -1.3+2.3+1.6-48.6=-46.0 ✓
    # Check 1: 1.3+2.3-1.6-48.6=-46.6 ✓
    # Check 20: 1.3*8000+2.3*400-32-48.6=10400+920-80.6=11239.4 ✓
    # Check 64: 1.3*262144+2.3*4096-102.4-48.6=340787.2+9420.8-151=350057.0 ✓
    # So formula: y = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 for all except x=100.
    # x=100: 1.3e6+23000-160-48.6=1322791.4 but observed 7772.9. Special region!
    # 7772.9... what could give that? Maybe a different formula near 100.
    # Only one point in special region. Need to guess boundaries. 
    # Maybe region is around 100. 7772.9 = ? 100^2*0.777? Or maybe it's x^3/... 
    # 7772.9 ≈ 100^2 * 0.77729. Or 100^3/1286. Hmm.
    # Could be a "hole" region. Maybe |x-100|<something. 
    # 7772.9... note 100^2=10000, 7772.9/10000=0.77729. 
    # Or maybe it's sin/cos related? Or maybe it's 100^3 * 0.0077729?
    # Actually 7772.9 could be 1.3*100^3*... no.
    # Let's guess: maybe near 100 the function is different. Without more data, guess region is x in [90,110] or similar.
    # Actually maybe the special region is where x^3 overflows? No.
    # 7772.9 = ? sqrt? 88.16^2=7772. Hmm.
    # Maybe it's x^2 * something. 7772.9/100 = 77.729. 
    # Could be a different cubic: maybe y = x^3/... 
    # Let's just mark it as uncertain. Perhaps the special interval is around 100, say [95,105], with unknown behavior.
    # Actually, maybe the special region is where the function is x^2*... Let's guess y = 0.77729*x^2 in that region? 
    # Or maybe it's a "reset" - like modulo. 100^3 mod something?
    # 100^3 = 1000000. 1000000 mod 7772.9? no.
    # Let's just guess the special region is [90,110] and formula there is unknown; 
    # but we need a guess. 7772.9 ≈ 100^3 * 0.0077729. Hmm.
    # Actually maybe it's 1.3x^3+2.3x^2-1.6x-48.6 but with x replaced by something. 
    # Or maybe the special region uses a different polynomial. 
    # Best guess: region around 100 where output is much smaller. 
    # Let me try: maybe near 100, y = x^2 * 0.77729? At x=100 that's 7772.9. 
    # Or maybe y = 1.3*(x-100)^3 + ... no.
    # I'll guess special region is [95,105] with y = 0.77729*x^2 (uncertain).
    # Actually, let me reconsider. 7772.9... could it be 100^3/128.6? 1000000/128.6=7776. close.
    # Or 100^2 * (something). 
    # Given only one data point, I'll mark it as uncertain region.
    # Maybe the region is where x^3 term is dropped? 2.3*10000-1.6*100-48.6=23000-160-48.6=22791.4 no.
    # Maybe y = 2.3x^2-1.6x-48.6? =23000-160-48.6=22791.4 no.
    # Maybe y = 1.3x^2-1.6x-48.6? =13000-160-48.6=12791.4 no.
    # Maybe y = 0.77729*x^2. I'll go with that as a guess.
    # Actually, 7772.9 = 100^2 * 0.77729. Hmm 0.77729... 
    # Or maybe it's 1.3*100^3 mod something? 
    # I'll just implement: if 95<=x<=105, use 0.77729*x^2 (guess).
    # Actually wait - maybe the special region is much wider. Let me check if 64 and 128 fit main formula - yes they do.
    # So region is between 64 and 128, containing 100. Could be [80,120] or [90,110].
    # I'll guess [90,110] and formula 0.77729*x^2.
    def main(x):
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    def special(x):
        return 0.77729*x**2  # ? uncertain
    out = []
    for x in probe["x"]:
        if 90 <= x <= 110:
            out.append(special(x))
        else:
            out.append(main(x))
    return {"y": out}
