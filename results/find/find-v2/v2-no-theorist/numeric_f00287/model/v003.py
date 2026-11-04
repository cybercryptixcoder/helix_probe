def predict(probe):
    # Left region x <= -5.5: f(x) = -0.7 * x  [E2: -120->84, -10->7; E6: -6->4.2, -5.5->4.2]
    #   E6 shows -5.5 -> 4.2 = -0.7*-5.5 = 3.85? No, 4.2. Hmm.
    #   Actually -5.5 -> 4.2 equals -0.7*-6. So left line uses ceil? -0.7*ceil(x)?
    #   Check E2: -120->84=-0.7*-120 (ceil=-120). -10->7=-0.7*-10. -20->14. All integers, can't tell.
    #   E1: -20.3->14.21? observed 14.21? E1 -20.3 -> ? Not shown fully. 
    #   E6: -6->4.2, -5.5->4.2. If f=-0.7*ceil(x): -6->4.2, -5.5->ceil=-5 -> 3.5. No.
    #   If f=-0.7*round? -5.5 rounds to -6 (banker's) -> 4.2. Possible.
    #   Simpler: left line is -0.7*x but -5.5 gives 3.85, observed 4.2. So not plain.
    #   Maybe left region ends at -5.5 inclusive with value from -6? Or step.
    #   Let's just say x < -5: f=-0.7*x; but -5.5 contradicts. 
    #   Alternative: f = -0.7*floor(x) for x<0? -6->4.2, -5.5->floor=-6->4.2. Yes!
    #   Check E2: -120->84 (floor -120), -10->7 (floor -10). E1: -6->4.2 (floor -6). 
    #   E1 -20.3: floor=-21 -> 14.7? Need check. E1 -24.3: floor -25 ->17.5? 
    #   E1 -50.4: floor -51 -> 35.7? E1 -61.7: floor -62 ->43.4?
    #   Hmm can't verify E1 values. But floor hypothesis fits E6 nicely.
    #   Wait E5: -48.6->34.3. -0.7*-48.6=34.02. floor(-48.6)=-49 ->34.3. Yes! floor works.
    #   E5: -7.1->5.6? floor(-7.1)=-8 ->5.6. Yes! -16.9->11.9? floor=-17->11.9. Yes!
    #   E5: -102.2->72.1? floor=-103->72.1. Yes!
    #   So left region: f(x) = -0.7 * floor(x) for x < -5 (or wherever boundary).
    # Flat region: -5 <= x < 19: f ~ -402.3 (noisy)  [E4, E6: -5..18.75 all flat]
    #   E6: -5.0 -> -402.3494 (flat), -5.5 -> 4.2 (line). So boundary at -5.
    #   E6: 18.5->-402.412, 18.75->-302.4?? Wait 18.75 -> -302.4. That's odd.
    #   -302.4 = -16.8*18 = -302.4. So 18.75 uses floor 18? -16.8*18=-302.4. Yes!
    #   So right region starts earlier than 19! At 18.75 it's already right formula.
    #   E4: 18->-402.4158 (flat), 19->-319.2=-16.8*19. 
    #   E6: 18.5->-402.412 (flat), 18.75->-302.4=-16.8*18.
    #   So boundary between 18.5 and 18.75. Hmm. Maybe 18.6? Or the right region is x>=18.6?
    #   Wait -16.8*floor(18.75)=-16.8*18=-302.4. And -16.8*floor(18.5)=-16.8*18=-302.4 too, but 18.5 gave flat -402.4.
    #   So 18.5 flat, 18.75 right. Boundary in (18.5, 18.75].
    #   Hmm but E4 19->-319.2=-16.8*19. floor(19)=19. OK.
    #   Maybe boundary is at 18.6 or 18.7? Uncertain. Let's guess 18.6? 
    #   Actually maybe the flat region is x in [-5, 18.6) and right is x>=18.6.
    #   Or maybe there's something like: right region x>=18.6? Odd number.
    #   Alternatively the transition is at x where floor changes... 
    #   Let's reconsider: maybe right region formula is -16.8*floor(x) but only for x >= some threshold T in (18.5,18.75].
    #   Let's guess T=18.6? Mark uncertain.
    #   Actually could be T = 18.5+something. Let's just pick 18.6.
    #   Hmm, but maybe simpler: the flat region is [-5, 18.5] and right is (18.5, ...]. But 18.5 is flat, 18.75 right. So T in (18.5, 18.75].
    #   Let me guess T=18.6.
    # Right region x >= 18.6: f(x) = -16.8 * floor(x)  [E2,E3,E4,E5,E6]
    #   E2: 20->-336=-16.8*20, 30->-504, etc. E3: 30.3->-504=-16.8*30. E5: 28.4->-470.4=-16.8*28.
    #   E5: 47.1->-789.6=-16.8*47. 58.8->-974.4=-16.8*58. 102.1->-1713.6=-16.8*102.
    #   E5: 105.7->-1764=-16.8*105. 119.5->-1999.2=-16.8*119. All floor. Good.
    #   E6: 18.75->-302.4=-16.8*18. 19->-319.2=-16.8*19. Good.
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if x < -5:
                y = -0.7 * math.floor(x)
            elif x < 18.6:
                y = -402.3
            else:
                y = -16.8 * math.floor(x)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
