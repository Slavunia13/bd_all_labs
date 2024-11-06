create_test_data_queries = [
    # Создание маршрутов (10 маршрутов с указанием общего расстояния)
    "CREATE (r1:Route {route_id: 1, route_name: 'Маршрут 1', total_distance: 12.5})",
    "CREATE (r2:Route {route_id: 2, route_name: 'Маршрут 2', total_distance: 8.3})",
    "CREATE (r3:Route {route_id: 3, route_name: 'Маршрут 3', total_distance: 15.0})",
    "CREATE (r4:Route {route_id: 4, route_name: 'Маршрут 4', total_distance: 9.7})",
    "CREATE (r5:Route {route_id: 5, route_name: 'Маршрут 5', total_distance: 10.2})",
    "CREATE (r6:Route {route_id: 6, route_name: 'Маршрут 6', total_distance: 11.6})",
    "CREATE (r7:Route {route_id: 7, route_name: 'Маршрут 7', total_distance: 13.4})",
    "CREATE (r8:Route {route_id: 8, route_name: 'Маршрут 8', total_distance: 16.5})",
    "CREATE (r9:Route {route_id: 9, route_name: 'Маршрут 9', total_distance: 7.9})",
    "CREATE (r10:Route {route_id: 10, route_name: 'Маршрут 10', total_distance: 14.3})",

    # Создание остановок (30 остановок с порядковыми номерами для различных маршрутов)
    *[f"CREATE (s{i}:Stop {{stop_id: {i}, stop_name: 'Остановка {i}', stop_order: {i % 10 + 1}}})" for i in range(1, 31)],

    # Создание организаций (40 организаций, включая учебные заведения, магазины и офисы)
    "CREATE (o1:Organization {org_id: 1, org_name: 'Школа 1', type: 'учебное заведение'})",
    "CREATE (o2:Organization {org_id: 2, org_name: 'Университет', type: 'учебное заведение'})",
    "CREATE (o3:Organization {org_id: 3, org_name: 'Магазин 1', type: 'магазин'})",
    "CREATE (o4:Organization {org_id: 4, org_name: 'Магазин 2', type: 'магазин'})",
    "CREATE (o5:Organization {org_id: 5, org_name: 'Офис 1', type: 'офис'})",
    *[f"CREATE (o{i}:Organization {{org_id: {i}, org_name: 'Организация {i}', type: 'офис'}})" for i in range(6, 21)],
    *[f"CREATE (o{i}:Organization {{org_id: {i}, org_name: 'Магазин {i-20}', type: 'магазин'}})" for i in range(21, 31)],
    *[f"CREATE (o{i}:Organization {{org_id: {i}, org_name: 'Учебное заведение {i-30}', type: 'учебное заведение'}})" for i in range(31, 41)],

    # Связывание маршрутов с остановками, добавлено свойство расстояния на отношениях
    *[
        f"MATCH (r:Route {{route_id: {i % 10 + 1}}}), (s:Stop {{stop_id: {i + 1}}}) "
        f"CREATE (r)-[:HAS_STOP {{distance: {(i % 5 + 1) * 0.5 + 0.5}}}]->(s)"
        for i in range(30)
    ],

    # Связывание остановок с организациями
    *[
        f"MATCH (s:Stop {{stop_id: {i % 30 + 1}}}), (o:Organization {{org_id: {i % 40 + 1}}}) "
        f"CREATE (s)-[:LOCATED_NEAR]->(o)"
        for i in range(80)
    ]
]

