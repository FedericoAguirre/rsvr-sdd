-- select * from payments_payment;
-- delete from payments_payment where id =2;


select pr.created_at,
    r.client_id as reservation_client_id,
    c.first_name as client_first_name,
    c.last_name as client_last_name,
    c.mobile as client_mobile,
    pr.payment_id,
    p.payment_type,
    p.payment_identifier,
    p.amount as payment_amount,
    p.date as payment_date,
    p.class_slot_count,
    p.client_id as payment_client_id,
    pr.reservation_id,
    r.date as reservation_date,
    r.status as reservation_status,
    r.equipment_id,
    e.name as equipment_name,
    e.status as equipment_status
from payments_paymentreservation as pr
inner join payments_payment as p
on pr.payment_id = p.id
inner join reservations_reservation as r
on pr.reservation_id = r.id
inner join clients_client as c
on p.client_id = c.id
inner join equipment_equipment as e
on r.equipment_id = e.id;


-- select p.id as payment_id,
-- p.amount as payment_amount,
-- p.date as payment_date,
-- p.class_slot_count,
-- p.client_id as payment_client_id,
-- r.id as reservation_id,
-- r.date as reservation_date,
-- r.equipment_id,
-- r.client_id as reservation_client_id,
-- c.id as client_id,
-- c.first_name as client_first_name,
-- c.last_name as client_last_name,
-- c2.id as payment_client_id,
-- c2.first_name as payment_client_first_name,
-- c2.last_name as payment_client_last_name
-- from payments_payment p
-- inner JOIN reservations_reservation r
-- on p.id = r.id
-- inner JOIN clients_client c
-- on r.client_id = c.id
-- inner JOIN clients_client c2
-- on p.client_id = c2.id;


--delete from payments_payment;
--delete from reservations_reservation;
