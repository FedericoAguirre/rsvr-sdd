select p.id as payment_id,
p.amount as payment_amount,
p.date as payment_date,
p.class_slot_count,
p.client_id as payment_client_id,
r.id as reservation_id,
r.date as reservation_date,
r.equipment_id,
r.client_id as reservation_client_id,
c.id as client_id,
c.first_name as client_first_name,
c.last_name as client_last_name,
c2.id as payment_client_id,
c2.first_name as payment_client_first_name,
c2.last_name as payment_client_last_name
from payments_payment p
inner JOIN reservations_reservation r
on p.id = r.id
inner JOIN clients_client c
on r.client_id = c.id
inner JOIN clients_client c2
on p.client_id = c2.id;


--delete from payments_payment;
--delete from reservations_reservation;
