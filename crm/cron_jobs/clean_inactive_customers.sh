#!/bin/bash

MANAGE_PY="../../manage.py"

# Run shell and delete customers
deleted_count=$($MANAGE_PY shell -c "
import sys
from datetime import datetime, timedelta
from django.utils import timezone
from crm.models import Customer, Order

cutoff = timezone.now() - timedelta(days=365)

inactive_customers = Customer.objects.exclude(
    id__in=Order.objects.filter(order_date__gte=cutoff).values_list('customer_id', flat=True)
)

count = inactive_customers.count()
inactive_customers.delete()

print(count)
" 2>/dev/null)

# Log count with timestamp
echo \"\$(date '+%Y-%m-%d %H:%M:%S') - Deleted \$deleted_count inactive customers\" >> /tmp/customer_cleanup_log.txt

