-- Заполнение таблицы Class71
INSERT INTO
    Class71 (
        Class71_Code,
        Class71_Name_Level1,
        Class71_Name_Level2,
        Class71_Name_Level3,
        Class71_Name_Level4,
        Class71_Name_Level5,
        ClassNameShort
    )
VALUES (
        'C71_001',
        'Level1_Name1',
        'Level2_Name1',
        'Level3_Name1',
        'Level4_Name1',
        'Level5_Name1',
        'ShortName1'
    );

INSERT INTO
    Class71 (
        Class71_Code,
        Class71_Name_Level1,
        Class71_Name_Level2,
        Class71_Name_Level3,
        Class71_Name_Level4,
        Class71_Name_Level5,
        ClassNameShort
    )
VALUES (
        'C71_002',
        'Level1_Name2',
        'Level2_Name2',
        'Level3_Name2',
        'Level4_Name2',
        'Level5_Name2',
        'ShortName2'
    );

-- Заполнение таблицы Class305
INSERT INTO
    Class305 (
        Class305_Code,
        Class305_Name_Level1,
        Class305_Name_Level2
    )
VALUES (
        'C305_001',
        'Division1',
        'Department1'
    );

INSERT INTO
    Class305 (
        Class305_Code,
        Class305_Name_Level1,
        Class305_Name_Level2
    )
VALUES (
        'C305_002',
        'Division2',
        'Department2'
    );

-- Заполнение таблицы Class37
INSERT INTO
    Class37 (
        Class37_Code,
        Class37_Name_Level1,
        Class37_Name_Level2,
        Class37_Name_Level3,
        Class37_Name_Level4,
        Class37_Name_Level5,
        Class37_Name_Level6,
        Class37_Name_Level7
    )
VALUES (
        'C37_001',
        'Region1',
        'City1',
        'Area1',
        'Zone1',
        'SubZone1',
        'SubArea1',
        'SubRegion1'
    );

INSERT INTO
    Class37 (
        Class37_Code,
        Class37_Name_Level1,
        Class37_Name_Level2,
        Class37_Name_Level3,
        Class37_Name_Level4,
        Class37_Name_Level5,
        Class37_Name_Level6,
        Class37_Name_Level7
    )
VALUES (
        'C37_002',
        'Region2',
        'City2',
        'Area2',
        'Zone2',
        'SubZone2',
        'SubArea2',
        'SubRegion2'
    );

-- Заполнение таблицы DescKontrag
INSERT INTO
    DescKontrag (
        CliCode,
        CliHeadCode,
        Class71_Code,
        Class72_Code,
        Class42_Code,
        dateArbDelay,
        SuppCust,
        CancelPenaltySymb,
        CancelRsrvPenCliSymb,
        CliName,
        Class172_Code,
        Class173_Code,
        Class174_Code,
        CliStructName,
        CliInn,
        CliDeact,
        IsArbitration,
        DateCre
    )
VALUES (
        1,
        1,
        'C71_001',
        'C721',
        'C42_1',
        '2024-01-01',
        'Supplier1',
        'N',
        'Y',
        'Client1',
        '1721',
        '1731',
        '1741',
        'Struct1',
        'INN1',
        'N',
        'N',
        '2024-01-01'
    );

INSERT INTO
    DescKontrag (
        CliCode,
        CliHeadCode,
        Class71_Code,
        Class72_Code,
        Class42_Code,
        dateArbDelay,
        SuppCust,
        CancelPenaltySymb,
        CancelRsrvPenCliSymb,
        CliName,
        Class172_Code,
        Class173_Code,
        Class174_Code,
        CliStructName,
        CliInn,
        CliDeact,
        IsArbitration,
        DateCre
    )
VALUES (
        2,
        1,
        'C71_002',
        'C722',
        'C42_2',
        '2024-02-01',
        'Supplier2',
        'Y',
        'N',
        'Client2',
        '1722',
        '1732',
        '1742',
        'Struct2',
        'INN2',
        'N',
        'N',
        '2024-02-01'
    );

-- Заполнение таблицы RgdDivisDprt
INSERT INTO
    RgdDivisDprt (
        RgdCode,
        Class305_Code,
        Class305_Code_1
    )
VALUES (101, 'C305_001', 'D1');

INSERT INTO
    RgdDivisDprt (
        RgdCode,
        Class305_Code,
        Class305_Code_1
    )
VALUES (102, 'C305_002', 'D2');

-- Заполнение таблицы CliTurnoverDtl
INSERT INTO
    public.CliTurnoverDtl (
        DataInfo,
        StoreCode,
        CliCode,
        RgdCode,
        ManCode,
        Class37_Code,
        Class55_Code,
        TypeMan,
        PrjCode,
        TenderCode,
        IsProject,
        IsTender,
        Nelikvid,
        StoreCode1F,
        ChannelSale,
        SumSaled,
        Cost,
        SumRB,
        QuantInv,
        CostAcc,
        QuantRgd,
        TranspExpense,
        CostOnShip,
        CostRegional,
        Cost81Orig,
        NumKey,
        YearInfo,
        QuartInfo,
        MonthInfo,
        CostAccOnDtInfo,
        TypeLogin,
        WayToLuggInBasket,
        CostForecastAccOnDtInfo,
        ObjCode,
        TypeLogin1,
        CostDSM,
        IsCompl,
        ShipmentSrc,
        SalesChannel,
        SalesSubChannel,
        PlanDelivDate,
        TypeExpDelivDate,
        ActDateOrdReady,
        MethReceivingReq,
        TypeReq,
        FirmPpl
    )
VALUES (
        '2024-01-01',
        'Store001',
        1,
        101,
        201,
        'C37_001',
        '55',
        'Type1',
        301,
        401,
        'N',
        'N',
        'N',
        'Store001F',
        'Online',
        1000.0,
        800.0,
        50.0,
        20.0,
        500.0,
        10.0,
        30.0,
        700.0,
        200.0,
        600.0,
        1,
        2024,
        1,
        1,
        100.0,
        'Login1',
        'Basket1',
        120.0,
        501,
        'LoginA',
        130.0,
        'N',
        'Src1',
        '1',
        'l1',
        '2024-01-15',
        601,
        '2024-01-10',
        701,
        801,
        901
    );

INSERT INTO
    public.CliTurnoverDtl (
        DataInfo,
        StoreCode,
        CliCode,
        RgdCode,
        ManCode,
        Class37_Code,
        Class55_Code,
        TypeMan,
        PrjCode,
        TenderCode,
        IsProject,
        IsTender,
        Nelikvid,
        StoreCode1F,
        ChannelSale,
        SumSaled,
        Cost,
        SumRB,
        QuantInv,
        CostAcc,
        QuantRgd,
        TranspExpense,
        CostOnShip,
        CostRegional,
        Cost81Orig,
        NumKey,
        YearInfo,
        QuartInfo,
        MonthInfo,
        CostAccOnDtInfo,
        TypeLogin,
        WayToLuggInBasket,
        CostForecastAccOnDtInfo,
        ObjCode,
        TypeLogin1,
        CostDSM,
        IsCompl,
        ShipmentSrc,
        SalesChannel,
        SalesSubChannel,
        PlanDelivDate,
        TypeExpDelivDate,
        ActDateOrdReady,
        MethReceivingReq,
        TypeReq,
        FirmPpl
    )
VALUES (
        '2024-02-01',
        'Store002',
        2,
        102,
        202,
        'C37_002',
        '56',
        'Type2',
        302,
        402,
        'Y',
        'Y',
        'Y',
        'Store002F',
        'Offline',
        1500.0,
        1000.0,
        60.0,
        30.0,
        600.0,
        20.0,
        40.0,
        800.0,
        300.0,
        700.0,
        2,
        2024,
        2,
        2,
        200.0,
        'Login2',
        'Basket2',
        220.0,
        502,
        'LoginB',
        230.0,
        'Y',
        'Src2',
        '2',
        'l2',
        '2024-02-15',
        602,
        '2024-02-10',
        702,
        802,
        902
    );