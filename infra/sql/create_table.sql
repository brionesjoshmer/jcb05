*********************************************************
* Create a table by executing the quey below with SQLDB Query Editor.*
*********************************************************

DROP TABLE IF EXISTS dbo.temphumid;
CREATE TABLE dbo.temphumid (
    id INT IDENTITY(1,1) NOT NULL,
    temperature NVARCHAR(20),
    humidity NVARCHAR(20),
    EventProcessedUtcTime DATETIME,
    PartitionId INT,
    EventEnqueuedUtcTime DATETIME,
    IoTHub_MessageId NVARCHAR(250),
    IoTHub_CorrelationId NVARCHAR(250),
    IoTHub_ConnectionDeviceId NVARCHAR(250),
    IoTHub_ConnectionDeviceGenerationId NVARCHAR(250),
    IoTHub_EnqueuedTime DATETIME
);