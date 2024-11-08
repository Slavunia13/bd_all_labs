queries_for_lab5 = {
    "Получить последовательность остановок для заданного маршрута.": '''
    MATCH (r:Route {route_id: __1})-[:HAS_STOP]->(s:Stop)    
    RETURN s.stop_name AS Название_остановки, s.stop_order AS Порядковый_номер   
    ORDER BY s.stop_order 
    ''',

    "Получить названия организаций, расположенных рядом с заданной остановкой.": '''
    MATCH (s:Stop {stop_id: __1})-[:LOCATED_NEAR]->(o:Organization) 
    RETURN o.org_name AS Название_организации 
    ''',

    "Найти все названия остановок, на которых возможны пересадки на другой маршрут.": '''
    MATCH (s:Stop)<-[:HAS_STOP]-(r:Route) 
    WITH s, COUNT(r) AS Количество_маршрутов 
    WHERE Количество_маршрутов > 1 
    RETURN s.stop_name AS Название_остановки 
    ''',

    "Найти все названия остановок, на которых останавливается только один маршрут.": '''
    MATCH (s:Stop)<-[:HAS_STOP]-(r:Route) 
    WITH s, COUNT(r) AS Количество_маршрутов 
    WHERE Количество_маршрутов = 1 
    RETURN s.stop_name AS Название_остановки 
    ''',

    "Найти названия учебных организаций и названия остановок, около которых они расположены.": '''
    MATCH (s:Stop)-[:LOCATED_NEAR]->(o:Organization {type: 'учебное заведение'}) 
    RETURN o.org_name AS Название_учебной_организации, s.stop_name AS Название_остановки 
    ''',

    "Получить все маршруты от одной заданной остановки до другой заданной остановки.": '''
    MATCH (r:Route)-[:HAS_STOP]->(s1:Stop {stop_id: __1}), 
          (r)-[:HAS_STOP]->(s2:Stop {stop_id: __2}) 
    WHERE s1.stop_order < s2.stop_order 
    RETURN r.route_name AS Маршрут, s1.stop_name AS Начальная_остановка, s2.stop_name AS Конечная_остановка 
    ''',

    "Получить минимальный по количеству остановок маршрут от одной заданной остановки до другой заданной остановки.": '''
    MATCH (r:Route)-[:HAS_STOP]->(s1:Stop {stop_id: __1}), 
          (r)-[:HAS_STOP]->(s2:Stop {stop_id: __2}) 
    WHERE s1.stop_order < s2.stop_order 
    RETURN r.route_name AS Маршрут, s1.stop_name AS Начальная_остановка, s2.stop_name AS Конечная_остановка, 
           (s2.stop_order - s1.stop_order) AS Количество_остановок 
    ORDER BY Количество_остановок ASC 
    LIMIT 1
    ''',

    "Получить все маршруты, которые проходят через 3 заданные остановки.": '''
    MATCH (r:Route)-[:HAS_STOP]->(s1:Stop {stop_id: __1}), 
          (r)-[:HAS_STOP]->(s2:Stop {stop_id: __2}), 
          (r)-[:HAS_STOP]->(s3:Stop {stop_id: __3}) 
    RETURN r.route_name AS Маршрут 
    ''',

    "Получить маршрут, который проходит рядом с максимальным количеством магазинов.": '''
    MATCH (r:Route)-[:HAS_STOP]->(s:Stop)-[:LOCATED_NEAR]->(o:Organization {type: 'магазин'}) 
    WITH r, COUNT(o) AS Количество_магазинов 
    RETURN r.route_name AS Маршрут 
    ORDER BY Количество_магазинов DESC 
    LIMIT 1
    ''',

    "Получить минимальный по расстоянию маршрут от одной заданной остановки до другой заданной остановки.": '''
    MATCH (r:Route)-[hs1:HAS_STOP]->(s1:Stop {stop_id: __1}), 
          (r)-[hs2:HAS_STOP]->(s2:Stop {stop_id: __2}) 
    WHERE hs1.stop_order < hs2.stop_order 
    WITH r, SUM(hs1.distance + hs2.distance) AS Общее_расстояние 
    RETURN r.route_name AS Маршрут, Общее_расстояние 
    ORDER BY Общее_расстояние ASC 
    LIMIT 1
    ''',

    "Найти названия организаций, расположенных рядом с третьей по счету остановкой от заданной остановки.": '''
    MATCH (r:Route)-[:HAS_STOP]->(s1:Stop {stop_id: __1}), 
          (r)-[:HAS_STOP]->(s2:Stop) 
    WHERE s1.stop_order + 3 = s2.stop_order 
    MATCH (s2)-[:LOCATED_NEAR]->(o:Organization) 
    RETURN o.org_name AS Название_организации 
    ''',

    "Найти все маршруты, длина которых превышает 10 км.": '''
    MATCH (r:Route) 
    WHERE r.total_distance > 10 
    RETURN r.route_name AS Маршрут, r.total_distance AS Длина_маршрута 
    '''
}
