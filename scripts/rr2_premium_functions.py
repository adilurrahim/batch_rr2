import numpy as np
def RiverClass(floodDepthDiff):
    if floodDepthDiff >= 0 and floodDepthDiff < 1:
        riverClass = "A"
    elif floodDepthDiff >= 1 and floodDepthDiff < 2:
        riverClass = "B"
    elif floodDepthDiff >= 2 and floodDepthDiff < 3:
        riverClass = "C"
    elif floodDepthDiff >= 3 and floodDepthDiff < 4:
        riverClass = "D"
    elif floodDepthDiff >= 4 and floodDepthDiff < 5:
        riverClass = "E"
    elif floodDepthDiff >= 5 and floodDepthDiff < 6:
        riverClass = "F"
    elif floodDepthDiff >= 6 and floodDepthDiff < 7:
        riverClass = "G"
    elif floodDepthDiff >= 7 and floodDepthDiff < 8:
        riverClass = "H"
    elif floodDepthDiff >= 8:
        riverClass = "I" 
    return riverClass

def CRS(crs):
    if crs == 1:
        crs_discount = 45
    elif crs == 2:
        crs_discount = 40
    elif crs == 3:
        crs_discount = 35
    elif crs == 4:
        crs_discount = 30
    elif crs == 5:
        crs_discount = 25
    elif crs == 6:
        crs_discount = 20
    elif crs == 7:
        crs_discount = 15
    elif crs == 8:
        crs_discount = 10
    elif crs == 9:
        crs_discount = 5
    elif crs == 10:
        crs_discount = 0  
    return crs_discount

def rr2Levee(inputs, tables_L, tables_BA, tables_PA):
    #Base Rate
    base_rate = tables_L["BaseRates"]
    base_rate_data = (base_rate[(base_rate['Region']==inputs['State']) & (base_rate['Single & 2-4 Family Home Indicator'] == inputs['SingleFamilyHomeIndicator'])])
    
    item1 = "Base Rate (per $1000 of Coverage Value)"
    #segment = base_rate_data.iloc[0]['Segment']  
    baserateResults_dict = {"items": item1,
                            "ifFluvialBuilding": base_rate_data.iloc[0,3], "ifFluvialContents": base_rate_data.iloc[0,4],
                            "ifPluvialBuilding": base_rate_data.iloc[0,5], "ifPluvialContents": base_rate_data.iloc[0,6],
                            "ssBuilding": base_rate_data.iloc[0,7], "ssContents": base_rate_data.iloc[0,8],
                            "ceBuilding": base_rate_data.iloc[0,13], "ceContents": base_rate_data.iloc[0,14],
                            "allPerils": ''}

    #DTR
    disttoriver = tables_L["DTR"]

    fluvial_dtr = np.interp([inputs['DTR']],(disttoriver[disttoriver.columns[0]]),(disttoriver[disttoriver.columns[1]]))[0]
    pluvial_dtr = np.interp([inputs['DTR']],(disttoriver[disttoriver.columns[0]]),(disttoriver[disttoriver.columns[2]]))[0]
    
    item2 = "Distance to River"
    distToRiverResults_dict = {"items": item2,
                               "ifFluvialBuilding": fluvial_dtr, "ifFluvialContents": fluvial_dtr,
                               "ifPluvialBuilding": pluvial_dtr, "ifPluvialContents": pluvial_dtr,
                               "ssBuilding": '', "ssContents": '',
                               "ceBuilding": '', "ceContents": '',
                               "allPerils": ''}

    
    #Elevation Relative ot River
    elevRiver = tables_L["ERR"]
    riverClass = RiverClass(inputs['RiverClass'])
    
    elevRiver = elevRiver[(elevRiver['River Class']== 'Class '+riverClass)]
    
    fluvial_err = np.interp([inputs['ERR']],(elevRiver[elevRiver.columns[1]]), (elevRiver[elevRiver.columns[2]]))[0]  
    pluvial_err = np.interp([inputs['ERR']],(elevRiver[elevRiver.columns[1]]), (elevRiver[elevRiver.columns[3]]))[0]   
    
    item3 = "Elevation Relative to River by River Class"
    elevRelToRiverResults_dict = {"items": item3,
                                  "ifFluvialBuilding": fluvial_err, "ifFluvialContents": fluvial_err,
                                  "ifPluvialBuilding": pluvial_err, "ifPluvialContents": pluvial_err,
                                  "ssBuilding": '', "ssContents": '',
                                  "ceBuilding": '', "ceContents": '',
                                  "allPerils": ''}

    #Structural Relative Elevation
    strucRelElv = tables_L["SructRelElev"]

    fluvial_sre = np.interp([inputs['StructRelElev']],(strucRelElv[strucRelElv.columns[0]]),(strucRelElv[strucRelElv.columns[1]]))[0]
    pluvial_sre = np.interp([inputs['StructRelElev']],(strucRelElv[strucRelElv.columns[0]]),(strucRelElv[strucRelElv.columns[2]]))[0]
    
    item4 = "Structural Relative Elevation"
    strucRelElvResults_dict = {"items": item4,
                               "ifFluvialBuilding": fluvial_sre, "ifFluvialContents": fluvial_sre,
                               "ifPluvialBuilding": pluvial_sre, "ifPluvialContents": pluvial_sre,
                               "ssBuilding": '', "ssContents": '',
                               "ceBuilding": '', "ceContents": '',
                               "allPerils": ''}
    
    #DTC
    distToCoastSS = tables_L["DTC_SS"]
    distToCoastCE = tables_L["DTC_CE"]
   
    distToCoastSS = distToCoastSS[distToCoastSS['Region']==inputs['State']]
    
    if inputs['DTC']<80467 and inputs['Elevation']<40:
        coastSS = np.interp([inputs['DTC']],(distToCoastSS[distToCoastSS.columns[1]]),(distToCoastSS[distToCoastSS.columns[2]]))[0]
    else:
        coastSS = 0
    
    if inputs['DTC']<=100:
        coastCE = np.interp([inputs['DTC']],(distToCoastCE[distToCoastCE.columns[0]]),(distToCoastCE[distToCoastCE.columns[1]]))[0]
    else:
        coastCE = 0
    
    item5 = "Distance to Coast"
    distToCoastResults_dict = {"items": item5,
                               "ifFluvialBuilding": '', "ifFluvialContents": '',
                               "ifPluvialBuilding": '', "ifPluvialContents": '',
                               "ssBuilding": coastSS, "ssContents": coastSS,
                               "ceBuilding": coastCE, "ceContents": coastCE,
                               "allPerils": ''}
    
    #Elevation
    Elev = tables_L["Elev_IFSS"]  
    
    Elev = Elev[Elev['Region']==inputs['State']]
    
    fluvial_elev = np.interp([inputs['Elevation']],(Elev[Elev.columns[1]]),(Elev[Elev.columns[2]]))[0]
    pluvial_elev = np.interp([inputs['Elevation']],(Elev[Elev.columns[1]]),(Elev[Elev.columns[3]]))[0]
    ss_elev = np.interp([inputs['Elevation']],(Elev[Elev.columns[1]]),(Elev[Elev.columns[4]]))[0]
    
    item6 = "Elevation"
    elevationResults_dict = {"items": item6,
                             "ifFluvialBuilding": fluvial_elev, "ifFluvialContents": fluvial_elev,
                             "ifPluvialBuilding": pluvial_elev, "ifPluvialContents": pluvial_elev,
                             "ssBuilding": ss_elev, "ssContents": ss_elev,
                             "ceBuilding": '', "ceContents": '',
                             "allPerils": ''}

    # Levee Quality
    leveeQualIF = tables_L["Levee_IF"]
    leveeQualSS = tables_L["Levee_SS"]
    
    leveeQualIF = leveeQualIF[leveeQualIF['Levee System ID']==inputs['LeveeSystemId']]
    leveeQualSS = leveeQualSS[leveeQualSS['Levee System ID']==inputs['LeveeSystemId']]
    
    if_levee = leveeQualIF.iloc[0,3]
    
    
    item7 = "Levee Quality"
    leveeQualityResults_dict = {"items": item7,
                                "ifFluvialBuilding": if_levee, "ifFluvialContents": if_levee,
                                "ifPluvialBuilding": '', "ifPluvialContents": '',
                                "ssBuilding": '', "ssContents": '',
                                "ceBuilding": '', "ceContents": '',
                                "allPerils": ''}
    
    #Territory
    territory = tables_L["Territory_IFSS"]
    
    territory = territory[(territory['HUC12']==inputs['HUC12'])&(territory['Levee System ID']==inputs['LeveeSystemId'])]
    
    if_territory = territory.iloc[0,2]
    ss_territory = territory.iloc[0,3]
    
    item8 = "Territory (HUC12 & Barrier Island Indicator)"
    territoryResults_dict = {"items": item8,
                             "ifFluvialBuilding": if_territory, "ifFluvialContents": if_territory,
                             "ifPluvialBuilding": if_territory, "ifPluvialContents": if_territory,
                             "ssBuilding": ss_territory, "ssContents": ss_territory,
                             "ceBuilding": '', "ceContents": '',
                             "allPerils": ''}

    #type of use
    type_use = tables_BA["typeUse"]
    type_use = type_use[type_use['Type of Use']== inputs['TypeofUse']]
    
    if_typeUse = type_use.iloc[0,1]
    ss_typeUse = type_use.iloc[0,2]
    
    item9 = "Type of Use"
    typeOfUseResults_dict = {"items": item9,
                             "ifFluvialBuilding": if_typeUse, "ifFluvialContents":if_typeUse,
                             "ifPluvialBuilding": if_typeUse, "ifPluvialContents": if_typeUse,
                             "ssBuilding": ss_typeUse, "ssContents":ss_typeUse,
                             "ceBuilding": '', "ceContents": '',
                             "allPerils": ''}
    #Floors of interest
    floor_int = tables_BA["floorInterest"]
    
    floor_int = floor_int[(floor_int['Single & 2-4 Family Home Indicator']==inputs['SingleFamilyHomeIndicator'])
                          & (floor_int['Condo Unit Owner Indicator']==inputs['CondoUnitOwnerIndicator'])
                          & (floor_int['Floors of Interest']==str(inputs['FloorofInterest']))]
    
    all_floorInterest = floor_int.iloc[0,3]
    item10 = "Floor of Interest"
    floorsOfIntResults_dict = {"items": item10,
                               "ifFluvialBuilding": all_floorInterest, "ifFluvialContents": all_floorInterest,
                               "ifPluvialBuilding": all_floorInterest, "ifPluvialContents": all_floorInterest,
                               "ssBuilding": all_floorInterest, "ssContents": all_floorInterest,
                               "ceBuilding": '', "ceContents": '',
                               "allPerils": ''}

    #Foundation type
    foundation = tables_BA["foundationType"]
    foundation = foundation[(foundation['Foundation Type']== inputs['FoundationType'])]
    
    all_foundation = foundation.iloc[0,1]
    item11 = "Foundation Type"
    foundationResults_dict = {"items": item11,
                              "ifFluvialBuilding": all_foundation, "ifFluvialContents": all_foundation,
                              "ifPluvialBuilding": all_foundation, "ifPluvialContents": all_foundation,
                              "ssBuilding": all_foundation, "ssContents": all_foundation,
                              "ceBuilding": '', "ceContents": '',
                              "allPerils": ''}

    #ffh
    ffh = tables_BA["firstfloorHeight"]
    
    column = ['First Floor Height (feet)']
    if inputs['FloodVents'] == "Yes":
        column.append(inputs['FoundationDesign'] + " With Flood Vents")
    else:
        column.append(inputs['FoundationDesign'] + " No Flood Vents")
    
    ffh = ffh[column]
    
    all_ffh = np.interp([inputs['ffh']],(ffh[ffh.columns[0]]),(ffh[ffh.columns[1]]))[0]
    
    item12 = "First Floor Height by Foundation Design"
    firstFloorHeightResults_dict = {"items": item12,
                                    "ifFluvialBuilding": all_ffh, "ifFluvialContents": all_ffh,
                                    "ifPluvialBuilding": all_ffh, "ifPluvialContents": all_ffh,
                                    "ssBuilding": all_ffh, "ssContents": all_ffh,
                                    "ceBuilding": '', "ceContents": '',
                                    "allPerils": ''}

    ##Coverage value
    buildingRCV = tables_BA["buildingValue"]
    contentsRCV = tables_BA["contentsValue"]
    
    #Capping
    RCVCaps = tables_BA["RCV_Caps"]
    RCVCaps = RCVCaps[RCVCaps["Type of Use"]==inputs["TypeofUse"]]

    buildingValue = [inputs['BuildingValue'] if inputs['BuildingValue']<int(RCVCaps.iloc[0,1]) else int(RCVCaps.iloc[0,1])][0]
    contentsValue = [inputs['ContentsValue'] if inputs['ContentsValue']<int(RCVCaps.iloc[0,2]) else int(RCVCaps.iloc[0,2])][0]
    
    building = np.interp([buildingValue],(buildingRCV[buildingRCV.columns[0]]),(buildingRCV[buildingRCV.columns[1]]))[0]
    content = np.interp([contentsValue],(contentsRCV[contentsRCV.columns[0]]),(contentsRCV[contentsRCV.columns[1]]))[0]

    item13 = "Coverage Value Factor"
    coverageValueFactorResults_dict = {"items": item13,
                                       "ifFluvialBuilding": building, "ifFluvialContents": content,
                                       "ifPluvialBuilding": building, "ifPluvialContents": content,
                                       "ssBuilding": building, "ssContents": content,
                                       "ceBuilding": '', "ceContents": '',
                                       "allPerils": ''}

    ##Deductible & Limit to coverage value ratio
    deductible_limit_coverage_A = tables_PA["deductible_limit_coverage_A"]
    deductible_limit_coverage_C = tables_PA["deductible_limit_coverage_C"]
    
    deductibleA = [inputs['deductibleA'] if inputs['deductibleA']>1000 and inputs['deductibleA']<10000  else 1000 if inputs['deductibleA']<1000 else 10000][0]
    deductibleC = [inputs['deductibleC'] if inputs['deductibleC']>1000 and inputs['deductibleC']<10000  else 1000 if inputs['deductibleC']<1000 else 10000][0]
    
    ratio_A = max(min((deductibleA + inputs['coverageA']) / buildingValue, 1), 0)  
    ratio_C = max(min((deductibleC + inputs['coverageC']) / contentsValue, 1), 0)  
    
    build_limit_if = np.interp([ratio_A],(deductible_limit_coverage_A[deductible_limit_coverage_A.columns[0]]),(deductible_limit_coverage_A[deductible_limit_coverage_A.columns[1]]))[0]
    build_limit_ss_ce = np.interp([ratio_A],(deductible_limit_coverage_A[deductible_limit_coverage_A.columns[0]]),(deductible_limit_coverage_A[deductible_limit_coverage_A.columns[2]]))[0]
    cont_limit_if = np.interp([ratio_C],(deductible_limit_coverage_C[deductible_limit_coverage_C.columns[0]]),(deductible_limit_coverage_C[deductible_limit_coverage_C.columns[1]]))[0]
    cont_limit_ss_ce = np.interp([ratio_C],(deductible_limit_coverage_C[deductible_limit_coverage_C.columns[0]]),(deductible_limit_coverage_C[deductible_limit_coverage_C.columns[2]]))[0]
    
    # item14 = "Deductible & Limit to Coverage Value Ratio"
    # deductibleLimittoCoverageValueResults_dict = {"items": item14,
    #                                               "ifFluvialBuilding": build_limit_if, "ifFluvialContents": cont_limit_if,
    #                                               "ifPluvialBuilding": build_limit_if, "ifPluvialContents": cont_limit_if,
    #                                               "ssBuilding": build_limit_ss_ce, "ssContents": cont_limit_ss_ce,
    #                                               "ceBuilding": build_limit_ss_ce, "ceContents": cont_limit_ss_ce,
    #                                               "allPerils": ''}

    ###
    deductible_coverage_A = tables_PA["deductible_coverage_A"]
    deductible_coverage_C = tables_PA["deductible_coverage_C"]
    
    ratio_A = max(min((deductibleA) / buildingValue, 1), 0)  
    ratio_C = max(min((deductibleC) / contentsValue, 1), 0)  
    
    build_if = np.interp([ratio_A],(deductible_coverage_A[deductible_coverage_A.columns[0]]),(deductible_coverage_A[deductible_coverage_A.columns[1]]))[0]
    build_ss_ce = np.interp([ratio_A],(deductible_coverage_A[deductible_coverage_A.columns[0]]),(deductible_coverage_A[deductible_coverage_A.columns[2]]))[0]
    cont_if = np.interp([ratio_C],(deductible_coverage_C[deductible_coverage_C.columns[0]]),(deductible_coverage_C[deductible_coverage_C.columns[1]]))[0]
    cont_ss_ce = np.interp([ratio_C],(deductible_coverage_C[deductible_coverage_C.columns[0]]),(deductible_coverage_C[deductible_coverage_C.columns[2]]))[0]
    
    final_ITV_build_if = [max(0.001,(build_limit_if - build_if)) if inputs['coverageA']>0 else 0][0]
    final_ITV_cont_if = [max(0.001,(cont_limit_if - cont_if)) if inputs['coverageC']>0 else 0][0]
    final_ITV_build_ss_ce = [max(0.001,(build_limit_ss_ce - build_ss_ce)) if inputs['coverageA']>0 else 0][0]
    final_ITV_cont_ss_ce = [max(0.001,(cont_limit_ss_ce - cont_ss_ce)) if inputs['coverageC']>0 else 0][0]
    
    item15 = "Final Deductible & ITV"
    finalDeductibleITVResults_dict = {"items": item15,
                                  "ifFluvialBuilding": final_ITV_build_if, "ifFluvialContents": final_ITV_cont_if,
                                  "ifPluvialBuilding": final_ITV_build_if, "ifPluvialContents": final_ITV_cont_if,
                                  "ssBuilding": final_ITV_build_ss_ce, "ssContents": final_ITV_cont_ss_ce,
                                  "ceBuilding": final_ITV_build_ss_ce, "ceContents": final_ITV_cont_ss_ce,
                                  "allPerils": ''}

    #Concentration Risk
    conc_risk_mapping = tables_PA["concriskMapping"]
    conc_risk = tables_PA["concRisk"]
    
    conc_risk_mapping = conc_risk_mapping[(conc_risk_mapping[conc_risk_mapping.columns[0]]== inputs['State(Long)']) & (conc_risk_mapping[conc_risk_mapping.columns[1]]== inputs['County'])]
    msa = conc_risk_mapping.iloc[0,2]
    
    conc_risk = conc_risk[(conc_risk[conc_risk.columns[0]]== msa)]
            
    conc_if = conc_risk.iloc[0,2]
    conc_ss = conc_risk.iloc[0,3]
    
    item16 = "Concentration Risk"  
    concRiskResults_dict = {"items": item16,
                            "ifFluvialBuilding": conc_if, "ifFluvialContents": conc_if,
                            "ifPluvialBuilding": conc_if, "ifPluvialContents": conc_if,
                            "ssBuilding": conc_ss, "ssContents": conc_ss,
                            "ceBuilding": '', "ceContents": '',
                            "allPerils": ''}

    # Geographic Rate by Peril & Coverage
    componentList = ['ifFluvialBuilding', 'ifFluvialContents', 'ifPluvialBuilding', 'ifPluvialContents', 'ssBuilding', 'ssContents', 'ceBuilding', 'ceContents', 'allPerils']
    geographicRatebyPerilCoverage = []
    for x in componentList:
        geoRatingFuncList = [baserateResults_dict[x], distToRiverResults_dict[x], elevRelToRiverResults_dict[x], strucRelElvResults_dict[x],
                             distToCoastResults_dict[x], elevationResults_dict[x], leveeQualityResults_dict[x],territoryResults_dict[x]]
        y = 1
        for i in range(len(geoRatingFuncList)):
            if geoRatingFuncList[i] not in ['', -9999.0]:
                y *= geoRatingFuncList[i]
        geographicRatebyPerilCoverage.append(y)
   
    item17 = "Geographic Rate by Peril & Coverage"
    geographicRateResults_dict = {"items": item17,
                                  "ifFluvialBuilding": geographicRatebyPerilCoverage[0], "ifFluvialContents": geographicRatebyPerilCoverage[1],
                                  "ifPluvialBuilding": geographicRatebyPerilCoverage[2], "ifPluvialContents": geographicRatebyPerilCoverage[3],
                                  "ssBuilding": geographicRatebyPerilCoverage[4], "ssContents": geographicRatebyPerilCoverage[5],
                                  "ceBuilding": geographicRatebyPerilCoverage[6], "ceContents": geographicRatebyPerilCoverage[7],
                                  "allPerils": ''}


    # Rate by Peril & Coverage
    ratebyPerilCoverage = []
    for x in componentList:
        RatingFuncList = [geographicRateResults_dict[x], typeOfUseResults_dict[x], floorsOfIntResults_dict[x], foundationResults_dict[x], firstFloorHeightResults_dict[x],
                          coverageValueFactorResults_dict[x],  finalDeductibleITVResults_dict[x], concRiskResults_dict[x]]
        y = 1
        for i in range(len(RatingFuncList)):
            if RatingFuncList[i] not in ['', -9999.0]:
                y *= RatingFuncList[i]
        ratebyPerilCoverage.append(y)
    
    item17 = "Rate by Peril & Coverage"
    rateResults_dict = {"items": item17,
                                  "ifFluvialBuilding": ratebyPerilCoverage[0], "ifFluvialContents": ratebyPerilCoverage[1],
                                  "ifPluvialBuilding": ratebyPerilCoverage[2], "ifPluvialContents": ratebyPerilCoverage[3],
                                  "ssBuilding": ratebyPerilCoverage[4], "ssContents": ratebyPerilCoverage[5],
                                  "ceBuilding": ratebyPerilCoverage[6], "ceContents": ratebyPerilCoverage[7],
                                  "allPerils": ''}
    
    #Final rates
    building_componentList = [i for i in componentList if "Building" in i]
    Rate_building =    0
    for components in building_componentList:
        Rate_building += rateResults_dict[components]
    
    contents_componentList = [i for i in componentList if "Content" in i]
    Rate_contents =    0
    for components in contents_componentList:
        Rate_contents += rateResults_dict[components]

    # Weighted Deductible & ITV Factor (Building)
   
    weighted_deductible_building = 0   
    for components in building_componentList:
        weighted_deductible_building += (finalDeductibleITVResults_dict[components] * (rateResults_dict[components]/Rate_building))
                                             
    weighted_deductible_contents = 0   
    for components in contents_componentList:
        weighted_deductible_contents += (finalDeductibleITVResults_dict[components] * (rateResults_dict[components]/Rate_contents))


    final_rate_building = min(max(Rate_building,0),15*weighted_deductible_building) 
    final_rate_contents =  min(max(Rate_contents,0),15*weighted_deductible_contents) 
    
    coverage_building_thousands = buildingValue/1000
    coverage_contents_thousands = contentsValue/1000
    
    #Prior claims
    priorClaim = inputs['PriorClaim']
    prior_claim_premium = (2.0 * coverage_building_thousands * weighted_deductible_building * max(0, float(priorClaim)-1))

    ####Premiums
    if final_rate_contents == 0:
        building_premium = round((final_rate_building * coverage_building_thousands) + 130 + 62.99 + prior_claim_premium,0)
        contents_premium = 0
    else:
        building_premium = (final_rate_building * coverage_building_thousands) + 0.5 * (130 + 62.99 + prior_claim_premium)
        contents_premium = (final_rate_contents * coverage_contents_thousands) + 0.5 * (130 + 62.99 + prior_claim_premium)

    icc_premium = (1.9/100)*(building_premium+contents_premium)
    
    #mitigation discount
    # me = MEAboveFirstFloor.objects.filter(machineryEquipmentAboveFirstFloor=currentScenario.MandEID).all()
    # me_discount = (1-float(me.values()[0]['coastalErosion']))*100
    # if str(currentScenario.floodVentsID) == "Yes":
    #     fo = FloodOpeningDiscount.objects.filter(foundationTypes=currentScenario.foundationTypeID).all()
    #     ffhs = fo.values_list("FFH", flat=True)
    #     ffhs = list(ffhs)
    #     discounts = fo.values_list("Discount", flat=True)
    #     discounts = list(discounts)
    #     fo_discount = round(float(np.interp([firstFloorHeightCurrentScenario],ffhs, discounts)), 1)
    # else:
    #     fo_discount = 0
        
    # mitigation_discount_percentage = me_discount + fo_discount
    # mitigation_discount = round((mitigation_discount_percentage/100)*(building_premium+contents_premium+ icc_premium- 130 - 62.99),0)
    mitigation_discount = np.array(0.0)
    
    crsRating = CRS(inputs['CRS'])
    crs_discount = (crsRating/100) * (building_premium + contents_premium + icc_premium - 130 - 62.99 - mitigation_discount)
    
    full_risk_premium = (building_premium + contents_premium + icc_premium - mitigation_discount - crs_discount)

    return [building_premium,contents_premium,icc_premium,mitigation_discount,crs_discount,full_risk_premium]

def rr2NL(inputs, tables_NL, tables_BA, tables_PA):
    #Base Rate
    base_rate = tables_NL["BaseRates"]
    base_rate_data = (base_rate[(base_rate['Region']==inputs['State']) & (base_rate['Single & 2-4 Family Home Indicator'] == inputs['SingleFamilyHomeIndicator'])])
    
    item1 = "Base Rate (per $1000 of Coverage Value)"
    segment = "Segment "+ str(int( base_rate_data.iloc[0,1]))  
    baserateResults_dict = {"items": item1,
                            "ifBuilding": base_rate_data.iloc[0,3], "ifContents": base_rate_data.iloc[0,4],
                            "ssBuilding": base_rate_data.iloc[0,5], "ssContents": base_rate_data.iloc[0,6],
                            "ceBuilding": base_rate_data.iloc[0,13], "ceContents": base_rate_data.iloc[0,14],
                            "allPerils": ''}

    #DTR
    disttoriver = tables_NL["DTR"]
    disttoriver = disttoriver[disttoriver["Region"]==segment]
    if_dtr = np.interp([inputs['DTR']],(disttoriver[disttoriver.columns[1]]),(disttoriver[disttoriver.columns[2]]))[0]
    
    item2 = "Distance to River"
    distToRiverResults_dict = {"items": item2,
                               "ifBuilding": if_dtr, "ifContents": if_dtr,
                               "ssBuilding": '', "ssContents": '',
                               "ceBuilding": '', "ceContents": '',
                               "allPerils": ''}

    #Elevation Relative ot River
    elevRiver = tables_NL["ERR"]
    riverClass = 'Class '+RiverClass(inputs['RiverClass'])
    columns = ["Elevation Relative to River (feet)","Inland Flood " + segment]
    
    elevRiver = elevRiver[(elevRiver['River Class']== riverClass)][columns]
    if_err = np.interp([inputs['ERR']],(elevRiver[elevRiver.columns[0]]), (elevRiver[elevRiver.columns[1]]))[0]      

    item3 = "Elevation Relative to River by River Class"
    elevRelToRiverResults_dict = {"items": item3,
                                  "ifBuilding": if_err, "ifContents": if_err,
                                  "ssBuilding": '', "ssContents": '',
                                  "ceBuilding": '', "ceContents": '',
                                  "allPerils": ''}
    
    #Drainage Area
    drainArea = tables_NL["DrainageArea"]
    columns = ["Drainage Area (km2)","Inland Flood " + segment]
    drainArea = drainArea[columns]
    
    if_da = np.interp([inputs['DrainageArea']],(drainArea[drainArea.columns[0]]), (drainArea[drainArea.columns[1]]))[0] 
    
    item4 = "Drainage Area"
    drainageAreaResults_dict = {"items": item4,
                                "ifBuilding": if_da, "ifContents": if_da,
                                "ssBuilding": '', "ssContents": '',
                                "ceBuilding": '', "ceContents": '',
                                "allPerils": ''}
    
    #Structural Relative Elevation
    strucRelElv = tables_NL["SructRelElev"]
    strucRelElv = strucRelElv[strucRelElv["Region"]==segment]
    if_sre = np.interp([inputs['StructRelElev']],(strucRelElv[strucRelElv.columns[1]]),(strucRelElv[strucRelElv.columns[2]]))[0]
    
    item5 = "Structural Relative Elevation"
    strucRelElvResults_dict = {"items": item5,
                               "ifBuilding": if_sre, "ifContents": if_sre,
                               "ssBuilding": '', "ssContents": '',
                               "ceBuilding": '', "ceContents": '',
                               "allPerils": ''}
    
    #DTC
    distToCoastSS = tables_NL["DTC"]
    distToCoastCE = tables_NL["DTC_CE"]
   
    distToCoastSS = distToCoastSS[distToCoastSS['Region']==segment]
    
    if inputs['DTC']<80467 and inputs['Elevation']<40:
        coastSS = np.interp([inputs['DTC']],(distToCoastSS[distToCoastSS.columns[1]]),(distToCoastSS[distToCoastSS.columns[2]]))[0]
    else:
        coastSS = 0
    
    if inputs['DTC']<=100:
        coastCE = np.interp([inputs['DTC']],(distToCoastCE[distToCoastCE.columns[0]]),(distToCoastCE[distToCoastCE.columns[1]]))[0]
    else:
        coastCE = 0
    
    item6 = "Distance to Coast"
    distToCoastResults_dict = {"items": item6,
                               "ifBuilding": '', "ifContents": '',
                               "ssBuilding": coastSS, "ssContents": coastSS,
                               "ceBuilding": coastCE, "ceContents": coastCE,
                               "allPerils": ''}
    
    #Elevation
    Elev = tables_NL["Elev"]  
    Elev = Elev[Elev['Region']==segment]
    
    ss_elev = np.interp([inputs['Elevation']],(Elev[Elev.columns[1]]),(Elev[Elev.columns[2]]))[0]
    
    item7 = "Elevation"
    elevationResults_dict = {"items": item7,
                             "ifBuilding": '', "ifContents": '',
                             "ssBuilding": ss_elev, "ssContents": ss_elev,
                             "ceBuilding": '', "ceContents": '',
                             "allPerils": ''}
   
    #Territory
    territory = tables_NL["Territory"]
    territory = territory[territory['HUC12']==inputs['HUC12']]
    
    if_territory = territory.iloc[0,1]
    ss_territory = territory.iloc[0,2]
    
    item8 = "Territory (HUC12 & Barrier Island Indicator)"
    territoryResults_dict = {"items": item8,
                             "ifBuilding": if_territory, "ifContents": if_territory,
                             "ssBuilding": ss_territory, "ssContents": ss_territory,
                             "ceBuilding": '', "ceContents": '',
                             "allPerils": ''}

    #type of use
    type_use = tables_BA["typeUse"]
    type_use = type_use[type_use['Type of Use']== inputs['TypeofUse']]
    
    if_typeUse = type_use.iloc[0,1]
    ss_typeUse = type_use.iloc[0,2]
    
    item9 = "Type of Use"
    typeOfUseResults_dict = {"items": item9,
                             "ifBuilding": if_typeUse, "ifContents":if_typeUse,
                             "ssBuilding": ss_typeUse, "ssContents":ss_typeUse,
                             "ceBuilding": '', "ceContents": '',
                             "allPerils": ''}
    #Floors of interest
    floor_int = tables_BA["floorInterest"]
    
    floor_int = floor_int[(floor_int['Single & 2-4 Family Home Indicator']==inputs['SingleFamilyHomeIndicator'])
                          & (floor_int['Condo Unit Owner Indicator']==inputs['CondoUnitOwnerIndicator'])
                          & (floor_int['Floors of Interest']==str(inputs['FloorofInterest']))]
    
    all_floorInterest = floor_int.iloc[0,3]
    item10 = "Floor of Interest"
    floorsOfIntResults_dict = {"items": item10,
                               "ifBuilding": all_floorInterest, "ifContents": all_floorInterest,
                               "ssBuilding": all_floorInterest, "ssContents": all_floorInterest,
                               "ceBuilding": '', "ceContents": '',
                               "allPerils": ''}

    #Foundation type
    foundation = tables_BA["foundationType"]
    foundation = foundation[(foundation['Foundation Type']== inputs['FoundationType'])]
    
    all_foundation = foundation.iloc[0,1]
    item11 = "Foundation Type"
    foundationResults_dict = {"items": item11,
                              "ifBuilding": all_foundation, "ifContents": all_foundation,
                              "ssBuilding": all_foundation, "ssContents": all_foundation,
                              "ceBuilding": '', "ceContents": '',
                              "allPerils": ''}

    #ffh
    ffh = tables_BA["firstfloorHeight"]
    
    column = ['First Floor Height (feet)']
    if inputs['FloodVents'] == "Yes":
        column.append(inputs['FoundationDesign'] + " With Flood Vents")
    else:
        column.append(inputs['FoundationDesign'] + " No Flood Vents")
    
    ffh = ffh[column]
    
    all_ffh = np.interp([inputs['ffh']],(ffh[ffh.columns[0]]),(ffh[ffh.columns[1]]))[0]
    
    item12 = "First Floor Height by Foundation Design"
    firstFloorHeightResults_dict = {"items": item12,
                                    "ifBuilding": all_ffh, "ifContents": all_ffh,
                                    "ssBuilding": all_ffh, "ssContents": all_ffh,
                                    "ceBuilding": '', "ceContents": '',
                                    "allPerils": ''}

    ##Coverage value
    buildingRCV = tables_BA["buildingValue"]
    contentsRCV = tables_BA["contentsValue"]
    
    #Capping
    RCVCaps = tables_BA["RCV_Caps"]
    RCVCaps = RCVCaps[RCVCaps["Type of Use"]==inputs["TypeofUse"]]

    buildingValue = [inputs['BuildingValue'] if inputs['BuildingValue']<int(RCVCaps.iloc[0,1]) else int(RCVCaps.iloc[0,1])][0]
    contentsValue = [inputs['ContentsValue'] if inputs['ContentsValue']<int(RCVCaps.iloc[0,2]) else int(RCVCaps.iloc[0,2])][0]
    
    building = np.interp([buildingValue],(buildingRCV[buildingRCV.columns[0]]),(buildingRCV[buildingRCV.columns[1]]))[0]
    content = np.interp([contentsValue],(contentsRCV[contentsRCV.columns[0]]),(contentsRCV[contentsRCV.columns[1]]))[0]

    item13 = "Coverage Value Factor"
    coverageValueFactorResults_dict = {"items": item13,
                                       "ifBuilding": building, "ifContents": content,
                                       "ssBuilding": building, "ssContents": content,
                                       "ceBuilding": '', "ceContents": '',
                                       "allPerils": ''}

    ##Deductible & Limit to coverage value ratio
    deductible_limit_coverage_A = tables_PA["deductible_limit_coverage_A"]
    deductible_limit_coverage_C = tables_PA["deductible_limit_coverage_C"]
    
    deductibleA = [inputs['deductibleA'] if inputs['deductibleA']>1000 and inputs['deductibleA']<10000  else 1000 if inputs['deductibleA']<1000 else 10000][0]
    deductibleC = [inputs['deductibleC'] if inputs['deductibleC']>1000 and inputs['deductibleC']<10000  else 1000 if inputs['deductibleC']<1000 else 10000][0]
    
    ratio_A = max(min((deductibleA + inputs['coverageA']) / buildingValue, 1), 0)  
    ratio_C = max(min((deductibleC + inputs['coverageC']) / contentsValue, 1), 0)  
    
    build_limit_if = np.interp([ratio_A],(deductible_limit_coverage_A[deductible_limit_coverage_A.columns[0]]),(deductible_limit_coverage_A[deductible_limit_coverage_A.columns[1]]))[0]
    build_limit_ss_ce = np.interp([ratio_A],(deductible_limit_coverage_A[deductible_limit_coverage_A.columns[0]]),(deductible_limit_coverage_A[deductible_limit_coverage_A.columns[2]]))[0]
    cont_limit_if = np.interp([ratio_C],(deductible_limit_coverage_C[deductible_limit_coverage_C.columns[0]]),(deductible_limit_coverage_C[deductible_limit_coverage_C.columns[1]]))[0]
    cont_limit_ss_ce = np.interp([ratio_C],(deductible_limit_coverage_C[deductible_limit_coverage_C.columns[0]]),(deductible_limit_coverage_C[deductible_limit_coverage_C.columns[2]]))[0]
    
    # item14 = "Deductible & Limit to Coverage Value Ratio"
    # deductibleLimittoCoverageValueResults_dict = {"items": item14,
    #                                               "ifFluvialBuilding": build_limit_if, "ifFluvialContents": cont_limit_if,
    #                                               "ifPluvialBuilding": build_limit_if, "ifPluvialContents": cont_limit_if,
    #                                               "ssBuilding": build_limit_ss_ce, "ssContents": cont_limit_ss_ce,
    #                                               "ceBuilding": build_limit_ss_ce, "ceContents": cont_limit_ss_ce,
    #                                               "allPerils": ''}

    ###
    deductible_coverage_A = tables_PA["deductible_coverage_A"]
    deductible_coverage_C = tables_PA["deductible_coverage_C"]
    
    ratio_A = max(min((deductibleA) / buildingValue, 1), 0)  
    ratio_C = max(min((deductibleC) / contentsValue, 1), 0)  
    
    build_if = np.interp([ratio_A],(deductible_coverage_A[deductible_coverage_A.columns[0]]),(deductible_coverage_A[deductible_coverage_A.columns[1]]))[0]
    build_ss_ce = np.interp([ratio_A],(deductible_coverage_A[deductible_coverage_A.columns[0]]),(deductible_coverage_A[deductible_coverage_A.columns[2]]))[0]
    cont_if = np.interp([ratio_C],(deductible_coverage_C[deductible_coverage_C.columns[0]]),(deductible_coverage_C[deductible_coverage_C.columns[1]]))[0]
    cont_ss_ce = np.interp([ratio_C],(deductible_coverage_C[deductible_coverage_C.columns[0]]),(deductible_coverage_C[deductible_coverage_C.columns[2]]))[0]
    
    final_ITV_build_if = [max(0.001,(build_limit_if - build_if)) if inputs['coverageA']>0 else 0][0]
    final_ITV_cont_if = [max(0.001,(cont_limit_if - cont_if)) if inputs['coverageC']>0 else 0][0]
    final_ITV_build_ss_ce = [max(0.001,(build_limit_ss_ce - build_ss_ce)) if inputs['coverageA']>0 else 0][0]
    final_ITV_cont_ss_ce = [max(0.001,(cont_limit_ss_ce - cont_ss_ce)) if inputs['coverageC']>0 else 0][0]
    
    item15 = "Final Deductible & ITV"
    finalDeductibleITVResults_dict = {"items": item15,
                                  "ifBuilding": final_ITV_build_if, "ifContents": final_ITV_cont_if,
                                  "ssBuilding": final_ITV_build_ss_ce, "ssContents": final_ITV_cont_ss_ce,
                                  "ceBuilding": final_ITV_build_ss_ce, "ceContents": final_ITV_cont_ss_ce,
                                  "allPerils": ''}

    #Concentration Risk
    conc_risk_mapping = tables_PA["concriskMapping"]
    conc_risk = tables_PA["concRisk"]
    
    conc_risk_mapping = conc_risk_mapping[(conc_risk_mapping[conc_risk_mapping.columns[0]]== inputs['State(Long)']) & (conc_risk_mapping[conc_risk_mapping.columns[1]]== inputs['County'])]
    msa = conc_risk_mapping.iloc[0,2]
    
    conc_risk = conc_risk[(conc_risk[conc_risk.columns[0]]== msa)]
            
    conc_if = conc_risk.iloc[0,2]
    conc_ss = conc_risk.iloc[0,3]
    
    item16 = "Concentration Risk"  
    concRiskResults_dict = {"items": item16,
                            "ifBuilding": conc_if, "ifContents": conc_if,
                            "ssBuilding": conc_ss, "ssContents": conc_ss,
                            "ceBuilding": '', "ceContents": '',
                            "allPerils": ''}

    # Geographic Rate by Peril & Coverage
    componentList = ['ifBuilding', 'ifContents', 'ssBuilding', 'ssContents', 'ceBuilding', 'ceContents', 'allPerils']
    geographicRatebyPerilCoverage = []
    for x in componentList:
        geoRatingFuncList = [baserateResults_dict[x], distToRiverResults_dict[x], elevRelToRiverResults_dict[x], drainageAreaResults_dict[x],
                             strucRelElvResults_dict[x],distToCoastResults_dict[x], elevationResults_dict[x], territoryResults_dict[x]]
                              
        y = 1
        for i in range(len(geoRatingFuncList)):
            if geoRatingFuncList[i] not in ['', -9999.0]:
                y *= geoRatingFuncList[i]
        geographicRatebyPerilCoverage.append(y)
   
    item17 = "Geographic Rate by Peril & Coverage"
    geographicRateResults_dict = {"items": item17,
                                  "ifBuilding": geographicRatebyPerilCoverage[0], "ifContents": geographicRatebyPerilCoverage[1],
                                  "ssBuilding": geographicRatebyPerilCoverage[2], "ssContents": geographicRatebyPerilCoverage[3],
                                  "ceBuilding": geographicRatebyPerilCoverage[4], "ceContents": geographicRatebyPerilCoverage[5],
                                  "allPerils": ''}

    # Rate by Peril & Coverage
    ratebyPerilCoverage = []
    for x in componentList:
        RatingFuncList = [geographicRateResults_dict[x], typeOfUseResults_dict[x], floorsOfIntResults_dict[x], foundationResults_dict[x], firstFloorHeightResults_dict[x],
                          coverageValueFactorResults_dict[x],  finalDeductibleITVResults_dict[x], concRiskResults_dict[x]]
        y = 1
        for i in range(len(RatingFuncList)):
            if RatingFuncList[i] not in ['', -9999.0]:
                y *= RatingFuncList[i]
        ratebyPerilCoverage.append(y)
    
    item17 = "Rate by Peril & Coverage"
    rateResults_dict = {"items": item17,
                                  "ifBuilding": ratebyPerilCoverage[0], "ifContents": ratebyPerilCoverage[1],
                                  "ssBuilding": ratebyPerilCoverage[2], "ssContents": ratebyPerilCoverage[3],
                                  "ceBuilding": ratebyPerilCoverage[4], "ceContents": ratebyPerilCoverage[5],
                                  "allPerils": ''}
    
    #Final rates
    building_componentList = [i for i in componentList if "Building" in i]
    Rate_building =    0
    for components in building_componentList:
        Rate_building += rateResults_dict[components]
    
    contents_componentList = [i for i in componentList if "Content" in i]
    Rate_contents =    0
    for components in contents_componentList:
        Rate_contents += rateResults_dict[components]

    # Weighted Deductible & ITV Factor (Building)
    weighted_deductible_building = 0   
    for components in building_componentList:
        weighted_deductible_building += (finalDeductibleITVResults_dict[components] * (rateResults_dict[components]/Rate_building))
                                             
    weighted_deductible_contents = 0   
    for components in contents_componentList:
        weighted_deductible_contents += (finalDeductibleITVResults_dict[components] * (rateResults_dict[components]/Rate_contents))

    final_rate_building = min(max(Rate_building,0),15*weighted_deductible_building) 
    final_rate_contents =  min(max(Rate_contents,0),15*weighted_deductible_contents) 
    
    coverage_building_thousands = buildingValue/1000
    coverage_contents_thousands = contentsValue/1000
    
    #Prior claims
    priorClaim = inputs['PriorClaim']
    prior_claim_premium = (2.0 * coverage_building_thousands * weighted_deductible_building * max(0, float(priorClaim)-1))

    ####Premiums
    if final_rate_contents == 0:
        building_premium = (final_rate_building * coverage_building_thousands) + 130 + 62.99 + prior_claim_premium
        contents_premium = 0
    else:
        building_premium = (final_rate_building * coverage_building_thousands) + 0.5 * (130 + 62.99 + prior_claim_premium)
        contents_premium = (final_rate_contents * coverage_contents_thousands) + 0.5 * (130 + 62.99 + prior_claim_premium)

    icc_premium = (1.9/100)*(building_premium+contents_premium)
    
    #mitigation discount
    # me = MEAboveFirstFloor.objects.filter(machineryEquipmentAboveFirstFloor=currentScenario.MandEID).all()
    # me_discount = (1-float(me.values()[0]['coastalErosion']))*100
    # if str(currentScenario.floodVentsID) == "Yes":
    #     fo = FloodOpeningDiscount.objects.filter(foundationTypes=currentScenario.foundationTypeID).all()
    #     ffhs = fo.values_list("FFH", flat=True)
    #     ffhs = list(ffhs)
    #     discounts = fo.values_list("Discount", flat=True)
    #     discounts = list(discounts)
    #     fo_discount = round(float(np.interp([firstFloorHeightCurrentScenario],ffhs, discounts)), 1)
    # else:
    #     fo_discount = 0
        
    # mitigation_discount_percentage = me_discount + fo_discount
    # mitigation_discount = round((mitigation_discount_percentage/100)*(building_premium+contents_premium+ icc_premium- 130 - 62.99),0)
    mitigation_discount = np.array(0.0)
    
    crsRating = CRS(inputs['CRS'])
    crs_discount = (crsRating/100) * (building_premium + contents_premium + icc_premium - 130 - 62.99 - mitigation_discount)
    
    full_risk_premium = (building_premium + contents_premium + icc_premium - mitigation_discount - crs_discount)

    return [building_premium,contents_premium,icc_premium,mitigation_discount,crs_discount,full_risk_premium]
