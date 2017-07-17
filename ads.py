import connection

def get_ads(city):
    try:
        conn = connection.con()
        cur = conn.cursor()

        add = []
        if city!=None:
            cur.execute("SELECT * FROM ad WHERE load_place=%s",city)
        else:
            cur.execute("SELECT * FROM ad")
        for ad in cur:
            add.append(dict(id_ad=ad[0], id_сlient=ad[1], load_place=ad[2],
                            unload_place=ad[3],id_carcase=ad[4],load_date=ad[5],
                            unload_date=ad[6], id_type_product=ad[7], size_product=ad[8],
                            weight_product=ad[9], lenght=ad[10], width=ad[11], height=ad[12],
                            price=ad[13],payment=ad[14], documents=ad[15],calculus=ad[16],prepay=ad[17]))
    except:
        return 'server is unvailable'
    finally:
        return add
        conn.close()
