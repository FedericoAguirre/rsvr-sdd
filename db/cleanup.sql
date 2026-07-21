TRUNCATE TABLE payments_paymentreservation;


-- Restarts the payments_payment table

DELETE FROM payments_payment;
SELECT setval(pg_get_serial_sequence('payments_payment', 'id'), COALESCE(MAX(id), 0) + 1, false) 
FROM payments_payment;


-- Restarts the reservations_reservation table

DELETE FROM reservations_reservation;
SELECT setval(pg_get_serial_sequence('reservations_reservation', 'id'), COALESCE(MAX(id), 0) + 1, false) 
FROM reservations_reservation;


-- Restarts the clients_client table

-- DELETE FROM clients_client;
-- SELECT setval(pg_get_serial_sequence('clients_client', 'id'), COALESCE(MAX(id), 0) + 1, false) 
-- FROM clients_client;
