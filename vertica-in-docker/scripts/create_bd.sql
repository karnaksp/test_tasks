CREATE TABLE Class71 (
    Class71_Code varchar(10) PRIMARY KEY NOT NULL,
    Class71_Name_Level1 varchar(164),
    Class71_Name_Level2 varchar(164),
    Class71_Name_Level3 varchar(164),
    Class71_Name_Level4 varchar(164),
    Class71_Name_Level5 varchar(164),
    ClassNameShort varchar(100)
) UNSEGMENTED ALL NODES;

CREATE TABLE Class305 (
    Class305_Code varchar(12) PRIMARY KEY NOT NULL,
    Class305_Name_Level1 varchar(160),
    Class305_Name_Level2 varchar(160)
) UNSEGMENTED ALL NODES;

CREATE TABLE Class37 (
    Class37_Code varchar(18) PRIMARY KEY NOT NULL,
    Class37_Name_Level1 varchar(510),
    Class37_Name_Level2 varchar(510),
    Class37_Name_Level3 varchar(510),
    Class37_Name_Level4 varchar(510),
    Class37_Name_Level5 varchar(510),
    Class37_Name_Level6 varchar(510),
    Class37_Name_Level7 varchar(510)
) UNSEGMENTED ALL NODES;

CREATE TABLE DescKontrag (
    CliCode integer NOT NULL PRIMARY KEY,
    CliHeadCode integer NOT NULL,
    Class71_Code varchar(10) NOT NULL,
    Class72_Code varchar(4) NOT NULL,
    Class42_Code varchar(14),
    dateArbDelay DATE,
    SuppCust varchar(60),
    CancelPenaltySymb varchar(6),
    CancelRsrvPenCliSymb varchar(6),
    CliName varchar(510),
    Class172_Code varchar(4),
    Class173_Code varchar(4),
    Class174_Code varchar(4),
    CliStructName varchar(60),
    CliInn varchar(24),
    CliDeact varchar(1),
    IsArbitration varchar(1),
    DateCre DATE
) UNSEGMENTED ALL NODES;

CREATE TABLE RgdDivisDprt (
    RgdCode integer NOT NULL PRIMARY KEY,
    Class305_Code varchar(12) NOT NULL,
    Class305_Code_1 varchar(6) NOT NULL
);

CREATE TABLE public.CliTurnoverDtl (
    DataInfo DATE NOT NULL,
    StoreCode varchar(21) NOT NULL,
    CliCode int NOT NULL,
    RgdCode int NOT NULL,
    ManCode int NOT NULL,
    Class37_Code varchar(18),
    Class55_Code varchar(2),
    TypeMan varchar(8),
    PrjCode int,
    TenderCode int,
    IsProject varchar(6),
    IsTender varchar(6),
    Nelikvid varchar(2),
    StoreCode1F varchar(20),
    ChannelSale varchar(20),
    SumSaled float,
    Cost float,
    SumRB float,
    QuantInv float,
    CostAcc float,
    QuantRgd float,
    TranspExpense float,
    CostOnShip float,
    CostRegional float,
    Cost81Orig float,
    NumKey int NOT NULL,
    YearInfo int NOT NULL,
    QuartInfo int NOT NULL,
    MonthInfo int NOT NULL,
    CostAccOnDtInfo float,
    TypeLogin varchar(20),
    WayToLuggInBasket varchar(20),
    CostForecastAccOnDtInfo float,
    ObjCode int,
    TypeLogin1 varchar(20),
    CostDSM float,
    IsCompl varchar(6),
    ShipmentSrc varchar(5),
    SalesChannel varchar(6),
    SalesSubChannel varchar(8),
    PlanDelivDate DATE,
    TypeExpDelivDate integer,
    ActDateOrdReady DATE,
    MethReceivingReq integer,
    TypeReq integer,
    FirmPpl integer
)
PARTITION BY (CliTurnoverDtl.DataInfo)
GROUP BY (
        date_trunc (
            'year',
            CliTurnoverDtl.DataInfo
        )
    ) ActivePartitionCount 4;