-- Создание временной таблицы с отфильтрованными данными о грузообороте
CREATE LOCAL TEMP TABLE FilteredCliTurnoverDtl ON COMMIT PRESERVE ROWS AS
SELECT
    md5(DataInfo::VARCHAR || CliCode::VARCHAR || RgdCode::VARCHAR || Class37_Code || SalesChannel) AS row_id,
    DataInfo,
    CliCode,
    RgdCode,
    Class37_Code,
    SalesChannel,
    SumSaled
FROM public.CliTurnoverDtl
WHERE
    DataInfo >= CURRENT_DATE - INTERVAL '24 months';

-- Создание временной таблицы со сведениями о контрагентах
CREATE LOCAL TEMP
TABLE FilteredDescKontrag ON
COMMIT PRESERVE ROWS AS
SELECT CliCode, CliName, Class71_Code
FROM DescKontrag;

-- Создание временной таблицы с целевыми клиентскими группами
CREATE LOCAL TEMP
TABLE FilteredClass71 ON
COMMIT PRESERVE ROWS AS
SELECT Class71_Code, ClassNameShort
FROM Class71;

-- Создание временной таблицы с дивизионами и товарными отделами
CREATE LOCAL TEMP
TABLE FilteredRgdDivisDprt ON
COMMIT PRESERVE ROWS AS
SELECT RgdCode, Class305_Code
FROM RgdDivisDprt;

-- Создание временной таблицы с территориальной структурой
CREATE LOCAL TEMP
TABLE FilteredClass37 ON
COMMIT PRESERVE ROWS AS
SELECT
    Class37_Code,
    Class37_Name_Level1,
    Class37_Name_Level2
FROM Class37;

-- Создание временной таблицы с агрегированными данными
CREATE LOCAL TEMP
TABLE AggregatedData ON
COMMIT PRESERVE ROWS AS
SELECT
    EXTRACT(
        YEAR
        FROM DataInfo
    ) AS YEAR,
    EXTRACT(
        MONTH
        FROM DataInfo
    ) AS MONTH,
    EXTRACT(
        QUARTER
        FROM DataInfo
    ) AS QUARTER,
    CASE
        WHEN EXTRACT(
            MONTH
            FROM DataInfo
        ) IN (1, 2, 3, 4, 5, 6) THEN 'H1'
        ELSE 'H2'
    END AS HALFYEAR,
    CliCode,
    RgdCode,
    Class37_Code,
    SalesChannel,
    SUM(SumSaled) AS TotalSales
FROM FilteredCliTurnoverDtl
GROUP BY
    EXTRACT(
        YEAR
        FROM DataInfo
    ),
    EXTRACT(
        MONTH
        FROM DataInfo
    ),
    EXTRACT(
        QUARTER
        FROM DataInfo
    ),
    CASE
        WHEN EXTRACT(
            MONTH
            FROM DataInfo
        ) IN (1, 2, 3, 4, 5, 6) THEN 'H1'
        ELSE 'H2'
    END,
    CliCode,
    RgdCode,
    Class37_Code,
    SalesChannel;
-- Создание окончательной таблицы для витрины данных
CREATE TABLE Vitrina AS
SELECT
    ad.YEAR,
    ad.MONTH,
    ad.QUARTER,
    ad.HALFYEAR,
    SUBSTRING(
        dk.Class71_Code
        FROM 1 FOR 2
    ) AS ClientGroupCode,
    SUBSTRING(
        rd.Class305_Code
        FROM 1 FOR 3
    ) AS ProductDivisionCode,
    SUBSTRING(
        rd.Class305_Code
        FROM 1 FOR 6
    ) AS ProductDepartmentCode,
    SUBSTRING(
        c37.Class37_Code
        FROM 1 FOR 1
    ) AS ManagerRegionCode,
    SUBSTRING(
        c37.Class37_Code
        FROM 1 FOR 2
    ) AS ManagerCityCode,
    ad.SalesChannel,
    ad.TotalSales
FROM
    AggregatedData ad
    JOIN FilteredDescKontrag dk ON ad.CliCode = dk.CliCode
    JOIN FilteredClass71 c71 ON dk.Class71_Code = c71.Class71_Code
    JOIN FilteredRgdDivisDprt rd ON ad.RgdCode = rd.RgdCode
    JOIN FilteredClass37 c37 ON ad.Class37_Code = c37.Class37_Code;

DROP TABLE IF EXISTS FilteredCliTurnoverDtl;

DROP TABLE IF EXISTS FilteredDescKontrag;

DROP TABLE IF EXISTS FilteredClass71;

DROP TABLE IF EXISTS FilteredRgdDivisDprt;

DROP TABLE IF EXISTS FilteredClass305;

DROP TABLE IF EXISTS FilteredClass37;

DROP TABLE IF EXISTS AggregatedData;