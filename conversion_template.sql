DECLARE @tableName NVARCHAR(128) = 'TABLE_NAME';


-- Replace with your table name
DECLARE @sql NVARCHAR(MAX) = N'';


-- Iterate over each column in the specified table
SELECT
    @sql = @sql + 'ALTER TABLE ' + QUOTENAME(@tableName) + ' ALTER COLUMN ' + QUOTENAME(c.name) + ' DATETIME2' + CHAR(13)
FROM
    sys.columns c
    JOIN sys.types t ON c.user_type_id = t.user_type_id
WHERE
    c.object_id = OBJECT_ID(@tableName)
    AND c.name LIKE '%date%' -- Only columns with "date" in their name
    AND t.name IN (
        'nvarchar',
        'varchar',
        'char',
        'nchar',
        'text',
        'date',
        'datetime'
    ) -- Assume string types that need conversion
    AND c.name NOT IN (
        'OK_TO_UPDATE__C',
        'OK_TO_CREATE__C',
        'LASTCLOSEDATECHANGEDHISTORYID',
        'SEND_UPDATES_TO_CVRX_CLINICAL_TEAM__C',
        'PROGRAMMER_DATE_ERROR__C',
        'RRT_UPDATED_BY_USER_MANUAL__C',
        'SURGERYOWNERUPDATE__C'
    ) -- Execute the dynamically constructed SQL
    EXEC sp_executesql @sql;