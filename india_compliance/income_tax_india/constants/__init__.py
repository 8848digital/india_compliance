# Income Tax Act 1961 (pre FY 2026-27)
OLD_TDS_SECTIONS = [
    "192A",
    "192B",
    "193",
    "194",
    "194A",
    "194B",
    "194BA",
    "194BB",
    "194C",
    "194D",
    "194DA",
    "194EE",
    "194F",
    "194G",
    "194H",
    "194I",
    "194I(a)",
    "194I(b)",
    "194IA",
    "194IB",
    "194IC",
    "194JA",
    "194JB",
    "194K",
    "194LA",
    "194LBA",
    "194LBB",
    "194LBC",
    "194M",
    "194N",
    "194O",
    "194P",
    "194Q",
    "194R",
    "194S",
    "194T",
    "195",
    "206C(1H)",
]

# ITA 2025 section codes per IT Rules 2026 (effective from FY 2026-27)
NEW_TDS_SECTIONS = [
    # Salary - Section 392
    "1001",  # Salary - Govt employees (non-Union)
    "1002",  # Salary - non-Govt employees
    "1003",  # Salary - Indian Govt employees
    # Resident payments - Section 393(1)
<<<<<<< HEAD
    {
        "section_code": "1004",
        "section_name": "392(7)",
        "description": "Any payment of accumulated balance due to an employee",
    },
    {
        "section_code": "1005",
        "section_name": "393(1) [Table: Sl. No. 1(i)]",
        "description": "Commission or brokerage - insurance",
    },
    {
        "section_code": "1006",
        "section_name": "393(1) [Table: Sl. No. 1(ii)]",
        "description": "Commission or brokerage - others",
    },
    {
        "section_code": "1008",
        "section_name": "393(1) [Table: Sl. No. 2(ii).D(a)]",
        "description": "Rent on machinery etc.- specified person",
    },
    {
        "section_code": "1009",
        "section_name": "393(1) [Table: Sl. No. 2(ii).D(b)]",
        "description": "Rent other than machinery etc.- specified person",
    },
    {
        "section_code": "1011",
        "section_name": "393(1) [Table: Sl. No. 3(ii)]",
        "description": "Payment on any consideration, not being consideration in kind, under the agreement referred to in section 67(14).",
    },
    {
        "section_code": "1012",
        "section_name": "393(1) [Table: Sl. No. 3(iii)]",
        "description": "Payment of compensation on acquisition of certain immovable property",
    },
    {
        "section_code": "1013",
        "section_name": "393(1) [Table: Sl. No. 4(i)]",
        "description": (
            "Income payable to a resident assessee in respect of units of a specified Mutual Fund specified under"
            " Schedule VII [Table: Sl. No. 20 or 21] or units from the Administrator of the specified undertaking"
            " or units from specified company"
        ),
    },
    {
        "section_code": "1014",
        "section_name": "393(1) [Table: Sl. No. 4(ii)]",
        "description": "Certain income in the form of interest from units of a business trust to a resident unit holder",
    },
    {
        "section_code": "1015",
        "section_name": "393(1) [Table: Sl. No. 4(ii)]",
        "description": "Certain income in the form of dividend from units of a business trust to a resident unit holder",
    },
    {
        "section_code": "1016",
        "section_name": "393(1) [Table: Sl. No. 4(ii)]",
        "description": "Certain income in the form of renting from units of a business trust being a real estate investment trust to a resident unit holder",
    },
    {
        "section_code": "1017",
        "section_name": "393(1) [Table: Sl. No. 4(iii)]",
        "description": (
            "Any income, other than that proportion of income which is exempt under Schedule V [Table: Sl. No. 2],"
            " in respect of units of an investment fund specified in section 224, payable to its unitholder."
        ),
    },
    {
        "section_code": "1018",
        "section_name": "393(1) [Table: Sl. No. 4(iv)]",
        "description": "Any income, in respect of an investment in a securitisation trust specified in section 221 to an investor.",
    },
    {
        "section_code": "1019",
        "section_name": "393(1) [Table: Sl. No. 5(i)]",
        "description": "Any income by way of interest on securities",
    },
    {
        "section_code": "1020",
        "section_name": "393(1) [Table: Sl. No. 5(ii).D(a)]",
        "description": "Any income by way of interest other than interest on securities, in case of deductee/payee is a senior citizen",
    },
    {
        "section_code": "1021",
        "section_name": "393(1) [Table: Sl. No. 5(ii).D(b)]",
        "description": "Any income by way of interest other than interest on securities, in case of deductee/payee is other than senior citizen",
    },
    {
        "section_code": "1022",
        "section_name": "393(1) [Table: Sl. No. 5(iii)]",
        "description": "Any income being interest other than interest on securities",
    },
    {
        "section_code": "1023",
        "section_name": "393(1) [Table: Sl. No. 6(i).D(a)]",
        "description": (
            "Any sum for carrying out any work (including supply of labour for carrying out any work) in pursuance"
            " of a contract between the contractor and a designated person - if contractor is individual or Hindu"
            " undivided family"
        ),
    },
    {
        "section_code": "1024",
        "section_name": "393(1) [Table: Sl. No. 6(i).D(b)]",
        "description": (
            "Any sum for carrying out any work (including supply of labour for carrying out any work) in pursuance"
            " of a contract between the contractor and a designated person - if contractor is a person other than"
            " individual or Hindu undivided family"
        ),
    },
    {
        "section_code": "1026",
        "section_name": "393(1) [Table: Sl. No. 6(iii).D(a)]",
        "description": (
            "Any sum by way of (a) fees for technical services (not being a professional services); or (b) royalty"
            " in the nature of consideration for sale, distribution or exhibition of cinematographic films; or"
            " (c) payee, engaged only in the business of operation of call centre"
        ),
    },
    {
        "section_code": "1027",
        "section_name": "393(1) [Table: Sl. No. 6(iii).D(b)]",
        "description": "Any sum by way of (a) fees for professional services; or (b) any sum referred to in section 26(2)(h)",
    },
    {
        "section_code": "1028",
        "section_name": "393(1) [Table: Sl. No. 6(iii).D(b)]",
        "description": (
            "Any sum by way of remuneration or fees or commission by whatever name called, other than those on"
            " which tax is deductible under section 392, to a director of a company"
        ),
    },
    {
        "section_code": "1029",
        "section_name": "393(1) [Table: Sl. No. 7]",
        "description": "Any dividends (including on preference shares) declared.",
    },
    {
        "section_code": "1030",
        "section_name": "393(1) [Table: Sl. No. 8(i)]",
        "description": (
            "Any sum under a life insurance policy, including the sum allocated as bonus on such policy, other than"
            " the amount not includible in the total income under Schedule II [Table: Sl. No. 2]"
        ),
    },
    {
        "section_code": "1031",
        "section_name": "393(1) [Table: Sl. No. 8(ii)]",
        "description": "Any sum for purchase of any goods",
    },
    {
        "section_code": "1032",
        "section_name": "393(1) [Table: Sl. No. 8(iii)]",
        "description": "Any sum to a specified senior citizen",
    },
    {
        "section_code": "1033",
        "section_name": "393(1) [Table: Sl. No. 8(iv)]",
        "description": (
            "Any benefit or perquisite, whether convertible into money or not,"
            " arising from business or the exercise of a profession of any resident."
        ),
    },
    {
        "section_code": "1034",
        "section_name": "393(1) [Table: Sl. No. 8(iv)] Note 6",
        "description": (
            "Any benefit or perquisite, whether in cash or in kind or partly in cash and partly in kind, whether"
            " convertible into money or not, arising from business or the exercise of a profession of any resident."
        ),
    },
    {
        "section_code": "1035",
        "section_name": "393(1) [Table: Sl. No. 8(v)]",
        "description": (
            "Sale of goods or provision of services by an e-commerce participant, facilitated by an e-commerce"
            " operator through its digital or electronic facility or platform."
        ),
    },
    {
        "section_code": "1037",
        "section_name": "393(1) [Table: Sl. No. 8(vi)]",
        "description": "Any sum by way of consideration for transfer of a virtual digital asset by other than individual or Hindu undivided family.",
    },
    {
        "section_code": "1038",
        "section_name": "393(1) [Table: Sl. No. 8(vi)] Note 6",
        "description": (
            "Any sum by way of consideration, whether in cash or in kind or partly in cash"
            " and partly in kind, for transfer of a virtual digital asset."
        ),
    },
    # Non-resident payments - Section 393(2)
    {
        "section_code": "1039",
        "section_name": "393(2) [Table: Sl. No. 1]",
        "description": "Any income referred to in section 211",
    },
    {
        "section_code": "1040",
        "section_name": "393(2) [Table: Sl. No. 2]",
        "description": (
            "Any income by way of interest payable in respect of monies borrowed in foreign currency from a source"
            " outside India under eligible loan or bond arrangements"
        ),
    },
    {
        "section_code": "1041",
        "section_name": "393(2) [Table: Sl. No. 3]",
        "description": (
            "Any income by way of interest payable in respect of monies borrowed from a source outside India by way"
            " of issue of rupee denominated bond before the 1st July, 2023"
        ),
    },
    {
        "section_code": "1042",
        "section_name": "393(2) [Table: Sl. No. 4.E(a)]",
        "description": (
            "Any income by way of interest payable in respect of monies borrowed from a source outside India by way"
            " of issue of long-term bond or rupee denominated bond listed only on a recognised stock exchange in an"
            " IFSC, issued on or after 1st April, 2020 but before 1st July, 2023"
        ),
    },
    {
        "section_code": "1043",
        "section_name": "393(2) [Table: Sl. No. 4.E(b)]",
        "description": (
            "Any income by way of interest payable in respect of monies borrowed from a source outside India by way"
            " of issue of long-term bond or rupee denominated bond listed only on a recognised stock exchange in an"
            " IFSC, issued on or after 1st July, 2023"
        ),
    },
    {
        "section_code": "1044",
        "section_name": "393(2) [Table: Sl. No. 5]",
        "description": "Income by way of interest from infrastructure debt fund payable to a non-resident",
    },
    {
        "section_code": "1045",
        "section_name": "393(2) [Table: Sl. No. 6.E(a)]",
        "description": "Any distributed income referred to in section 223, being of the nature referred to in Schedule V [Table: Sl. No. 3.B(a)]",
    },
    {
        "section_code": "1046",
        "section_name": "393(2) [Table: Sl. No. 6.E(b)]",
        "description": "Any distributed income referred to in section 223, being of the nature referred to in Schedule V [Table: Sl. No. 3.B(b)]",
    },
    {
        "section_code": "1047",
        "section_name": "393(2) [Table: Sl. No. 7]",
        "description": "Any distributed income referred to in section 223, being of the nature referred to in Schedule V [Table: Sl. No. 4]",
    },
    {
        "section_code": "1048",
        "section_name": "393(2) [Table: Sl. No. 8]",
        "description": (
            "Any income, other than that proportion of income which is exempt under Schedule V [Table: Sl. No. 2],"
            " in respect of units of an investment fund specified in section 224"
        ),
    },
    {
        "section_code": "1049",
        "section_name": "393(2) [Table: Sl. No. 9]",
        "description": "Any income in respect of an investment in a securitisation trust specified in section 221",
    },
    {
        "section_code": "1050",
        "section_name": "393(2) [Table: Sl. No. 10]",
        "description": "Any income in respect of units of a specified Mutual Fund under Schedule VII [Table: Sl. No. 20 or 21], or from the specified company",
    },
    {
        "section_code": "1051",
        "section_name": "393(2) [Table: Sl. No. 11]",
        "description": "Any income in respect of units referred to in section 208",
    },
    {
        "section_code": "1052",
        "section_name": "393(2) [Table: Sl. No. 12]",
        "description": "Any income by way of long-term capital gains arising from the transfer of units referred to in section 208",
    },
    {
        "section_code": "1053",
        "section_name": "393(2) [Table: Sl. No. 13]",
        "description": "Any income by way of interest or dividends in respect of bonds or Global Depository Receipts referred to in section 209",
    },
    {
        "section_code": "1054",
        "section_name": "393(2) [Table: Sl. No. 14]",
        "description": (
            "Any income by way of long-term capital gains arising from the transfer of bonds"
            " or Global Depository Receipts referred to in section 209"
        ),
    },
    {
        "section_code": "1055",
        "section_name": "393(2) [Table: Sl. No. 15]",
        "description": "Any income in respect of securities referred to in section 210(1) [Table: Sl. No. 1]",
    },
    {
        "section_code": "1056",
        "section_name": "393(2) [Table: Sl. No. 16]",
        "description": "Any income in respect of securities referred to in section 210(1) [Table: Sl. No. 1]",
    },
    {
        "section_code": "1057",
        "section_name": "393(2) [Table: Sl. No. 17]",
        "description": (
            "Any interest (not being interest referred to against serial numbers 2, 3, 4 and 5) or any other sum"
            " chargeable under the provisions of this Act, not being income chargeable under the head Salaries"
        ),
    },
    # Any person payments - Section 393(3)
    {
        "section_code": "1058",
        "section_name": "393(3) [Table: Sl. No. 1]",
        "description": (
            "Any income by way of winnings (other than winnings from Sl. No. 2 of the table at section 393(3))"
            " from (a) any lottery; or (b) crossword puzzle; or (c) card game and other game of any sort; or"
            " (d) gambling or betting of any form or nature whatsoever"
        ),
    },
    {
        "section_code": "1059",
        "section_name": "393(3) [Table: Sl. No. 1] Note 2",
        "description": (
            "Any income by way of winnings (other than winnings from Sl. No. 2 of the table at section 393(3))"
            " from (a) any lottery; or (b) crossword puzzle; or (c) card game and other game of any sort; or"
            " (d) gambling or betting of any form or nature whatsoever where consideration is made in kind or cash"
            " is not sufficient to meet the tax liability and tax has been paid before such winnings are released"
        ),
    },
    {
        "section_code": "1060",
        "section_name": "393(3) [Table: Sl. No. 2]",
        "description": "Any income by way of winnings from online game.",
    },
    {
        "section_code": "1061",
        "section_name": "393(3) [Table: Sl. No. 2] Note 2",
        "description": (
            "Any income by way of winnings from online games, is made in kind or cash is not sufficient to meet"
            " the tax liability and tax has been paid before such winnings are released"
        ),
    },
    {
        "section_code": "1062",
        "section_name": "393(3) [Table: Sl. No. 3]",
        "description": "Any income by way of winnings from any horse race.",
    },
    {
        "section_code": "1063",
        "section_name": "393(3) [Table: Sl. No. 4]",
        "description": (
            "Any income, credited or paid to a person, who is or has been stocking, distributing, purchasing or"
            " selling lottery tickets, by way of commission, remuneration or prize (by whatever name called) on"
            " such tickets"
        ),
    },
    {
        "section_code": "1064",
        "section_name": "393(3) [Table: Sl. No. 5.D(a)]",
        "description": "Payment of certain amounts in cash by bank/post office/co-operative society to a deductee being a co-operative society",
    },
    {
        "section_code": "1065",
        "section_name": "393(3) [Table: Sl. No. 5.D(b)]",
        "description": (
            "Payment of certain amounts in cash by bank/post office/co-operative society"
            " to a deductee being a person other than co-operative society"
        ),
    },
    {
        "section_code": "1066",
        "section_name": "393(3) [Table: Sl. No. 6]",
        "description": "Any amount referred to in section 80CCA(2)(a) of the Income-tax Act, 1961 (43 of 1961) (as it existed prior to its repeal).",
    },
    {
        "section_code": "1067",
        "section_name": "393(3) [Table: Sl. No. 7]",
        "description": (
            "Any sum in the nature of salary, remuneration, commission, bonus or interest paid to a partner of the"
            " firm or credited to his account (including capital account)."
        ),
    },
    # Collection codes - Section 394(1)
    {
        "section_code": "1068",
        "section_name": "394(1) [Table: Sl. No. 1]",
        "description": "Sale of alcoholic liquor for human consumption",
    },
    {
        "section_code": "1069",
        "section_name": "394(1) [Table: Sl. No. 2]",
        "description": "Sale of tendu leaves",
    },
    {
        "section_code": "1070",
        "section_name": "394(1) [Table: Sl. No. 3]",
        "description": "Sale of timber obtained under a forest lease",
    },
    {
        "section_code": "1071",
        "section_name": "394(1) [Table: Sl. No. 3]",
        "description": "Sale of timber obtained by any mode other than a forest lease",
    },
    {
        "section_code": "1072",
        "section_name": "394(1) [Table: Sl. No. 3]",
        "description": "Sale of any other forest produce (not being timber or tendu leaves) obtained under a forest lease.",
    },
    {
        "section_code": "1073",
        "section_name": "394(1) [Table: Sl. No. 4]",
        "description": "Sale of scrap",
    },
    {
        "section_code": "1074",
        "section_name": "394(1) [Table: Sl. No. 5]",
        "description": "Sale of minerals, being coal or lignite or iron ore",
    },
    {
        "section_code": "1075",
        "section_name": "394(1) [Table: Sl. No. 6.D(a)]",
        "description": "Sale consideration exceeding threshold limit in case of sale of motor vehicle",
    },
    {
        "section_code": "1076",
        "section_name": "394(1) [Table: Sl. No. 6.D(b)]",
        "description": "Sale consideration exceeding threshold limit in case of sale of wrist watch",
    },
    {
        "section_code": "1077",
        "section_name": "394(1) [Table: Sl. No. 6.D(b)]",
        "description": "Sale consideration exceeding threshold limit in case of sale of art piece such as antiques, painting, sculpture",
    },
    {
        "section_code": "1078",
        "section_name": "394(1) [Table: Sl. No. 6.D(b)]",
        "description": "Sale consideration exceeding threshold limit in case of sale of collectibles such as coin, stamp",
    },
    {
        "section_code": "1079",
        "section_name": "394(1) [Table: Sl. No. 6.D(b)]",
        "description": "Sale consideration exceeding threshold limit in case of sale of yacht, rowing boat, canoe, helicopter",
    },
    {
        "section_code": "1080",
        "section_name": "394(1) [Table: Sl. No. 6.D(b)]",
        "description": "Sale consideration exceeding threshold limit in case of sale of pair of sunglasses",
    },
    {
        "section_code": "1081",
        "section_name": "394(1) [Table: Sl. No. 6.D(b)]",
        "description": "Sale consideration exceeding threshold limit in case of sale of bag such as handbag, purse",
    },
    {
        "section_code": "1082",
        "section_name": "394(1) [Table: Sl. No. 6.D(b)]",
        "description": "Sale consideration exceeding threshold limit in case of sale of pair of shoes",
    },
    {
        "section_code": "1083",
        "section_name": "394(1) [Table: Sl. No. 6.D(b)]",
        "description": "Sale consideration exceeding threshold limit in case of sale of sportswear and equipment such as golf kit, ski-wear",
    },
    {
        "section_code": "1084",
        "section_name": "394(1) [Table: Sl. No. 6.D(b)]",
        "description": "Sale consideration exceeding threshold limit in case of sale of home theatre system",
    },
    {
        "section_code": "1085",
        "section_name": "394(1) [Table: Sl. No. 6.D(b)]",
        "description": "Sale consideration exceeding threshold limit in case of sale of horse for horse racing in race clubs and horse for polo",
    },
    {
        "section_code": "1086",
        "section_name": "394(1) [Table: Sl. No. 7.D(a)]",
        "description": (
            "Remittance under the Liberalised Remittance Scheme of an amount or aggregate of the amounts exceeding"
            " threshold limit for purposes of education or medical treatment"
        ),
    },
    {
        "section_code": "1087",
        "section_name": "394(1) [Table: Sl. No. 7.D(b)]",
        "description": (
            "Remittance under the Liberalised Remittance Scheme of an amount or aggregate of the amounts exceeding"
            " threshold limit for purposes other than education or medical treatment"
        ),
    },
    {
        "section_code": "1088",
        "section_name": "394(1) [Table: Sl. No. 8.D(a)]",
        "description": (
            "Sale of overseas tour programme package including expenses for travel or hotel stay or boarding or"
            " lodging or any such similar or related expenditure with amount or aggregate of amounts up to threshold"
        ),
    },
    {
        "section_code": "1089",
        "section_name": "394(1) [Table: Sl. No. 8.D(b)]",
        "description": (
            "Sale of overseas tour programme package including expenses for travel or hotel stay or boarding or"
            " lodging or any such similar or related expenditure with amount or aggregate of amounts above threshold"
        ),
    },
    {
        "section_code": "1090",
        "section_name": "394(1) [Table: Sl. No. 9]",
        "description": "Use of parking lot for the purpose of business, excluding mining and quarrying of mineral oil (including petroleum and natural gas).",
    },
    {
        "section_code": "1091",
        "section_name": "394(1) [Table: Sl. No. 9]",
        "description": "Use of toll plaza for the purpose of business, excluding mining and quarrying of mineral oil (including petroleum and natural gas).",
    },
    {
        "section_code": "1092",
        "section_name": "394(1) [Table: Sl. No. 9]",
        "description": (
            "Use of mine or quarry for the purpose of business, excluding mining and"
            " quarrying of mineral oil (including petroleum and natural gas)."
        ),
    },
=======
    "1004": (
        "392(7)",
        "Any payment of accumulated balance due to an employee",
    ),
    "1005": (
        "393(1) [Table: Sl. No. 1(i)]",
        "Commission or brokerage - insurance",
    ),
    "1006": (
        "393(1) [Table: Sl. No. 1(ii)]",
        "Commission or brokerage - others",
    ),
    "1008": (
        "393(1) [Table: Sl. No. 2(ii).D(a)]",
        "Rent on machinery etc.- specified person",
    ),
    "1009": (
        "393(1) [Table: Sl. No. 2(ii).D(b)]",
        "Rent other than machinery etc.- specified person",
    ),
    "1011": (
        "393(1) [Table: Sl. No. 3(ii)]",
        "Payment on any consideration, not being consideration in kind, under the agreement referred to in section 67(14).",
    ),
    "1012": (
        "393(1) [Table: Sl. No. 3(iii)]",
        "Payment of compensation on acquisition of certain immovable property",
    ),
    "1013": (
        "393(1) [Table: Sl. No. 4(i)]",
        "Income payable to a resident assessee in respect of units of a specified Mutual Fund specified under"
        " Schedule VII [Table: Sl. No. 20 or 21] or units from the Administrator of the specified undertaking"
        " or units from specified company",
    ),
    "1014": (
        "393(1) [Table: Sl. No. 4(ii)]",
        "Certain income in the form of interest from units of a business trust to a resident unit holder",
    ),
    "1015": (
        "393(1) [Table: Sl. No. 4(ii)]",
        "Certain income in the form of dividend from units of a business trust to a resident unit holder",
    ),
    "1016": (
        "393(1) [Table: Sl. No. 4(ii)]",
        "Certain income in the form of renting from units of a business trust being a real estate investment trust to a resident unit holder",
    ),
    "1017": (
        "393(1) [Table: Sl. No. 4(iii)]",
        "Any income, other than that proportion of income which is exempt under Schedule V [Table: Sl. No. 2],"
        " in respect of units of an investment fund specified in section 224, payable to its unitholder.",
    ),
    "1018": (
        "393(1) [Table: Sl. No. 4(iv)]",
        "Any income, in respect of an investment in a securitisation trust specified in section 221 to an investor.",
    ),
    "1019": (
        "393(1) [Table: Sl. No. 5(i)]",
        "Any income by way of interest on securities",
    ),
    "1020": (
        "393(1) [Table: Sl. No. 5(ii).D(a)]",
        "Any income by way of interest other than interest on securities, in case of deductee/payee is a senior citizen",
    ),
    "1021": (
        "393(1) [Table: Sl. No. 5(ii).D(b)]",
        "Any income by way of interest other than interest on securities, in case of deductee/payee is other than senior citizen",
    ),
    "1022": ("393(1) [Table: Sl. No. 5(iii)]", "Any income being interest other than interest on securities"),
    "1023": (
        "393(1) [Table: Sl. No. 6(i).D(a)]",
        "Any sum for carrying out any work (including supply of labour for carrying out any work) in pursuance"
        " of a contract between the contractor and a designated person - if contractor is individual or Hindu"
        " undivided family",
    ),
    "1024": (
        "393(1) [Table: Sl. No. 6(i).D(b)]",
        "Any sum for carrying out any work (including supply of labour for carrying out any work) in pursuance"
        " of a contract between the contractor and a designated person - if contractor is a person other than"
        " individual or Hindu undivided family",
    ),
    "1026": (
        "393(1) [Table: Sl. No. 6(iii).D(a)]",
        "Any sum by way of (a) fees for technical services (not being a professional services); or (b) royalty"
        " in the nature of consideration for sale, distribution or exhibition of cinematographic films; or"
        " (c) payee, engaged only in the business of operation of call centre",
    ),
    "1027": (
        "393(1) [Table: Sl. No. 6(iii).D(b)]",
        "Any sum by way of (a) fees for professional services; or (b) any sum referred to in section 26(2)(h)",
    ),
    "1028": (
        "393(1) [Table: Sl. No. 6(iii).D(b)]",
        "Any sum by way of remuneration or fees or commission by whatever name called, other than those on"
        " which tax is deductible under section 392, to a director of a company",
    ),
    "1029": ("393(1) [Table: Sl. No. 7]", "Any dividends (including on preference shares) declared."),
    "1030": (
        "393(1) [Table: Sl. No. 8(i)]",
        "Any sum under a life insurance policy, including the sum allocated as bonus on such policy, other than"
        " the amount not includible in the total income under Schedule II [Table: Sl. No. 2]",
    ),
    "1031": ("393(1) [Table: Sl. No. 8(ii)]", "Any sum for purchase of any goods"),
    "1032": ("393(1) [Table: Sl. No. 8(iii)]", "Any sum to a specified senior citizen"),
    "1033": (
        "393(1) [Table: Sl. No. 8(iv)]",
        "Any benefit or perquisite, whether convertible into money or not, arising from business or the exercise of a profession of any resident.",
    ),
    "1034": (
        "393(1) [Table: Sl. No. 8(iv)] Note 6",
        "Any benefit or perquisite, whether in cash or in kind or partly in cash and partly in kind, whether"
        " convertible into money or not, arising from business or the exercise of a profession of any resident.",
    ),
    "1035": (
        "393(1) [Table: Sl. No. 8(v)]",
        "Sale of goods or provision of services by an e-commerce participant, facilitated by an e-commerce"
        " operator through its digital or electronic facility or platform.",
    ),
    "1037": (
        "393(1) [Table: Sl. No. 8(vi)]",
        "Any sum by way of consideration for transfer of a virtual digital asset by other than individual or Hindu undivided family.",
    ),
    "1038": (
        "393(1) [Table: Sl. No. 8(vi)] Note 6",
        "Any sum by way of consideration, whether in cash or in kind or partly in cash and partly in kind, for transfer of a virtual digital asset.",
    ),
    # Non-resident payments - Section 393(2)
    "1039": (
        "393(2) [Table: Sl. No. 1]",
        "Any income referred to in section 211",
    ),
    "1040": (
        "393(2) [Table: Sl. No. 2]",
        "Any income by way of interest payable in respect of monies borrowed in foreign currency from a source"
        " outside India under eligible loan or bond arrangements",
    ),
    "1041": (
        "393(2) [Table: Sl. No. 3]",
        "Any income by way of interest payable in respect of monies borrowed from a source outside India by way"
        " of issue of rupee denominated bond before the 1st July, 2023",
    ),
    "1042": (
        "393(2) [Table: Sl. No. 4.E(a)]",
        "Any income by way of interest payable in respect of monies borrowed from a source outside India by way"
        " of issue of long-term bond or rupee denominated bond listed only on a recognised stock exchange in an"
        " IFSC, issued on or after 1st April, 2020 but before 1st July, 2023",
    ),
    "1043": (
        "393(2) [Table: Sl. No. 4.E(b)]",
        "Any income by way of interest payable in respect of monies borrowed from a source outside India by way"
        " of issue of long-term bond or rupee denominated bond listed only on a recognised stock exchange in an"
        " IFSC, issued on or after 1st July, 2023",
    ),
    "1044": (
        "393(2) [Table: Sl. No. 5]",
        "Income by way of interest from infrastructure debt fund payable to a non-resident",
    ),
    "1045": (
        "393(2) [Table: Sl. No. 6.E(a)]",
        "Any distributed income referred to in section 223, being of the nature referred to in Schedule V [Table: Sl. No. 3.B(a)]",
    ),
    "1046": (
        "393(2) [Table: Sl. No. 6.E(b)]",
        "Any distributed income referred to in section 223, being of the nature referred to in Schedule V [Table: Sl. No. 3.B(b)]",
    ),
    "1047": (
        "393(2) [Table: Sl. No. 7]",
        "Any distributed income referred to in section 223, being of the nature referred to in Schedule V [Table: Sl. No. 4]",
    ),
    "1048": (
        "393(2) [Table: Sl. No. 8]",
        "Any income, other than that proportion of income which is exempt under Schedule V [Table: Sl. No. 2],"
        " in respect of units of an investment fund specified in section 224",
    ),
    "1049": (
        "393(2) [Table: Sl. No. 9]",
        "Any income in respect of an investment in a securitisation trust specified in section 221",
    ),
    "1050": (
        "393(2) [Table: Sl. No. 10]",
        "Any income in respect of units of a specified Mutual Fund under Schedule VII [Table: Sl. No. 20 or 21], or from the specified company",
    ),
    "1051": ("393(2) [Table: Sl. No. 11]", "Any income in respect of units referred to in section 208"),
    "1052": (
        "393(2) [Table: Sl. No. 12]",
        "Any income by way of long-term capital gains arising from the transfer of units referred to in section 208",
    ),
    "1053": (
        "393(2) [Table: Sl. No. 13]",
        "Any income by way of interest or dividends in respect of bonds or Global Depository Receipts referred to in section 209",
    ),
    "1054": (
        "393(2) [Table: Sl. No. 14]",
        "Any income by way of long-term capital gains arising from the transfer of bonds or Global Depository Receipts referred to in section 209",
    ),
    "1055": (
        "393(2) [Table: Sl. No. 15]",
        "Any income in respect of securities referred to in section 210(1) [Table: Sl. No. 1]",
    ),
    "1056": (
        "393(2) [Table: Sl. No. 16]",
        "Any income in respect of securities referred to in section 210(1) [Table: Sl. No. 1]",
    ),
    "1057": (
        "393(2) [Table: Sl. No. 17]",
        "Any interest (not being interest referred to against serial numbers 2, 3, 4 and 5) or any other sum"
        " chargeable under the provisions of this Act, not being income chargeable under the head Salaries",
    ),
    # Any person payments - Section 393(3)
    "1058": (
        "393(3) [Table: Sl. No. 1]",
        "Any income by way of winnings (other than winnings from Sl. No. 2 of the table at section 393(3))"
        " from (a) any lottery; or (b) crossword puzzle; or (c) card game and other game of any sort; or"
        " (d) gambling or betting of any form or nature whatsoever",
    ),
    "1059": (
        "393(3) [Table: Sl. No. 1] Note 2",
        "Any income by way of winnings (other than winnings from Sl. No. 2 of the table at section 393(3))"
        " from (a) any lottery; or (b) crossword puzzle; or (c) card game and other game of any sort; or"
        " (d) gambling or betting of any form or nature whatsoever where consideration is made in kind or cash"
        " is not sufficient to meet the tax liability and tax has been paid before such winnings are released",
    ),
    "1060": ("393(3) [Table: Sl. No. 2]", "Any income by way of winnings from online game."),
    "1061": (
        "393(3) [Table: Sl. No. 2] Note 2",
        "Any income by way of winnings from online games, is made in kind or cash is not sufficient to meet"
        " the tax liability and tax has been paid before such winnings are released",
    ),
    "1062": ("393(3) [Table: Sl. No. 3]", "Any income by way of winnings from any horse race."),
    "1063": (
        "393(3) [Table: Sl. No. 4]",
        "Any income, credited or paid to a person, who is or has been stocking, distributing, purchasing or"
        " selling lottery tickets, by way of commission, remuneration or prize (by whatever name called) on"
        " such tickets",
    ),
    "1064": (
        "393(3) [Table: Sl. No. 5.D(a)]",
        "Payment of certain amounts in cash by bank/post office/co-operative society to a deductee being a co-operative society",
    ),
    "1065": (
        "393(3) [Table: Sl. No. 5.D(b)]",
        "Payment of certain amounts in cash by bank/post office/co-operative society to a deductee being a person other than co-operative society",
    ),
    "1066": (
        "393(3) [Table: Sl. No. 6]",
        "Any amount referred to in section 80CCA(2)(a) of the Income-tax Act, 1961 (43 of 1961) (as it existed prior to its repeal).",
    ),
    "1067": (
        "393(3) [Table: Sl. No. 7]",
        "Any sum in the nature of salary, remuneration, commission, bonus or interest paid to a partner of the"
        " firm or credited to his account (including capital account).",
    ),
    # Collection codes - Section 394(1)
    "1068": (
        "394(1) [Table: Sl. No. 1]",
        "Sale of alcoholic liquor for human consumption",
    ),
    "1069": (
        "394(1) [Table: Sl. No. 2]",
        "Sale of tendu leaves",
    ),
    "1070": (
        "394(1) [Table: Sl. No. 3]",
        "Sale of timber obtained under a forest lease",
    ),
    "1071": (
        "394(1) [Table: Sl. No. 3]",
        "Sale of timber obtained by any mode other than a forest lease",
    ),
    "1072": (
        "394(1) [Table: Sl. No. 3]",
        "Sale of any other forest produce (not being timber or tendu leaves) obtained under a forest lease.",
    ),
    "1073": (
        "394(1) [Table: Sl. No. 4]",
        "Sale of scrap",
    ),
    "1074": (
        "394(1) [Table: Sl. No. 5]",
        "Sale of minerals, being coal or lignite or iron ore",
    ),
    "1075": (
        "394(1) [Table: Sl. No. 6.D(a)]",
        "Sale consideration exceeding threshold limit in case of sale of motor vehicle",
    ),
    "1076": (
        "394(1) [Table: Sl. No. 6.D(b)]",
        "Sale consideration exceeding threshold limit in case of sale of wrist watch",
    ),
    "1077": (
        "394(1) [Table: Sl. No. 6.D(b)]",
        "Sale consideration exceeding threshold limit in case of sale of art piece such as antiques, painting, sculpture",
    ),
    "1078": (
        "394(1) [Table: Sl. No. 6.D(b)]",
        "Sale consideration exceeding threshold limit in case of sale of collectibles such as coin, stamp",
    ),
    "1079": (
        "394(1) [Table: Sl. No. 6.D(b)]",
        "Sale consideration exceeding threshold limit in case of sale of yacht, rowing boat, canoe, helicopter",
    ),
    "1080": (
        "394(1) [Table: Sl. No. 6.D(b)]",
        "Sale consideration exceeding threshold limit in case of sale of pair of sunglasses",
    ),
    "1081": (
        "394(1) [Table: Sl. No. 6.D(b)]",
        "Sale consideration exceeding threshold limit in case of sale of bag such as handbag, purse",
    ),
    "1082": (
        "394(1) [Table: Sl. No. 6.D(b)]",
        "Sale consideration exceeding threshold limit in case of sale of pair of shoes",
    ),
    "1083": (
        "394(1) [Table: Sl. No. 6.D(b)]",
        "Sale consideration exceeding threshold limit in case of sale of sportswear and equipment such as golf kit, ski-wear",
    ),
    "1084": (
        "394(1) [Table: Sl. No. 6.D(b)]",
        "Sale consideration exceeding threshold limit in case of sale of home theatre system",
    ),
    "1085": (
        "394(1) [Table: Sl. No. 6.D(b)]",
        "Sale consideration exceeding threshold limit in case of sale of horse for horse racing in race clubs and horse for polo",
    ),
    "1086": (
        "394(1) [Table: Sl. No. 7.D(a)]",
        "Remittance under the Liberalised Remittance Scheme of an amount or aggregate of the amounts exceeding"
        " threshold limit for purposes of education or medical treatment",
    ),
    "1087": (
        "394(1) [Table: Sl. No. 7.D(b)]",
        "Remittance under the Liberalised Remittance Scheme of an amount or aggregate of the amounts exceeding"
        " threshold limit for purposes other than education or medical treatment",
    ),
    "1088": (
        "394(1) [Table: Sl. No. 8.D(a)]",
        "Sale of overseas tour programme package including expenses for travel or hotel stay or boarding or"
        " lodging or any such similar or related expenditure with amount or aggregate of amounts up to threshold",
    ),
    "1089": (
        "394(1) [Table: Sl. No. 8.D(b)]",
        "Sale of overseas tour programme package including expenses for travel or hotel stay or boarding or"
        " lodging or any such similar or related expenditure with amount or aggregate of amounts above threshold",
    ),
    "1090": (
        "394(1) [Table: Sl. No. 9]",
        "Use of parking lot for the purpose of business, excluding mining and quarrying of mineral oil (including petroleum and natural gas).",
    ),
    "1091": (
        "394(1) [Table: Sl. No. 9]",
        "Use of toll plaza for the purpose of business, excluding mining and quarrying of mineral oil (including petroleum and natural gas).",
    ),
    "1092": (
        "394(1) [Table: Sl. No. 9]",
        "Use of mine or quarry for the purpose of business, excluding mining and quarrying of mineral oil (including petroleum and natural gas).",
    ),
>>>>>>> dbf3292a (chore: codacy issue)
    # Form 141 sections (challan-cum-statement, no numeric return code)
    "393(1) Sl.2(i)",  # Rent by Individual/HUF (was 194IB)
    "393(1) Sl.3(i)",  # Immovable property transfer (was 194IA)
    "393(1) Sl.6(ii)",  # Contractor/professional by Ind/HUF >50L (was 194M)
]

TDS_SECTIONS = OLD_TDS_SECTIONS + NEW_TDS_SECTIONS

TDS_ENTITY_TYPE = ["Individual", "Company", "Company Assessee", "No PAN / Invalid PAN"]
