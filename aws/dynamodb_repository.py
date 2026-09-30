from datetime import datetime, timezone
from decimal import Decimal

import boto3


class DynamoDBMetricsRepository:
    def __init__(self, table_name: str, region: str):
        dynamodb = boto3.resource("dynamodb", region_name=region)
        self.table = dynamodb.Table(table_name)

    def put_category_metric(
        self,
        *,
        category: str,
        generation_count: int,
        ai_generation_count: int,
        average_rating: float | None,
    ) -> None:
        item = {
            "pk": f"CATEGORY#{category}",
            "sk": "LATEST",
            "category": category,
            "generation_count": generation_count,
            "ai_generation_count": ai_generation_count,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        if average_rating is not None:
            item["average_rating"] = Decimal(str(round(average_rating, 2)))

        self.table.put_item(Item=item)

    def get_category_metric(self, category: str) -> dict | None:
        response = self.table.get_item(
            Key={
                "pk": f"CATEGORY#{category}",
                "sk": "LATEST",
            }
        )
        return response.get("Item")
