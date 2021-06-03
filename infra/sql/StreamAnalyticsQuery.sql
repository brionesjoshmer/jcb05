********************************************************************
* The query below will be cerated in Stream Analytics by running a template   *
* (The query is written in a single line in template and hard to read, so it is transcribed here.) *
********************************************************************
SELECT
 TRY_CAST(input.temperature AS nvarchar(max)) AS temperature,
 TRY_CAST(input.humidity AS nvarchar(max)) AS humidity,
 TRY_CAST(input.EventProcessedUtcTime AS DATETIME) AS EventProcessedUtcTime,
 TRY_CAST(input.PartitionId AS bigint) AS PartitionId,
 TRY_CAST(input.EventEnqueuedUtcTime AS DATETIME) AS EventEnqueuedUtcTime,
 TRY_CAST(input.IoTHub.MessageId AS nvarchar(max)) AS IoTHub_MessageId,
 TRY_CAST(input.IoTHub.CorrelationId AS nvarchar(max)) AS IoTHub_CorrelationId,
 TRY_CAST(input.IoTHub.ConnectionDeviceId AS nvarchar(max)) AS IoTHub_ConnectionDeviceId,
 TRY_CAST(input.IoTHub.ConnectionDeviceGenerationId AS nvarchar(max)) AS IoTHub_ConnectionDeviceGenerationId,
 TRY_CAST(input.IoTHub.EnqueuedTime AS DATETIME) AS IoTHub_EnqueuedTime
INTO
 [sqldb]
FROM
 [iot-hub] as input

SELECT *
INTO
 [blobstorage]
FROM
 [iot-hub]

SELECT *
INTO
[event-hub]
FROM
 [iot-hub] as input
