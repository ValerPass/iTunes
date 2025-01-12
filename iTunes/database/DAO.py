from database.DB_connect import DBConnect
from model.album import Album

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAlbums(d):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT  a.* , sum(t.Milliseconds) as totD
                FROM album a , track t
                WHERE a.AlbumId = t.AlbumId 
                GROUP BY a.AlbumId 
                HAVING totD > %s"""

        cursor.execute(query, (d,))

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT distinctrow t1.AlbumId as a1, t2.AlbumId as a2
                FROM playlisttrack p1, track t2, track t1, playlisttrack p2
                WHERE p2.PlaylistId = p1.PlaylistId and p2.TrackId = t2.TrackId and p1.TrackId = t1.TrackId 
                #prendo le coppie di canzoni che fanno parte di una stessa playlist
                and t1.AlbumId < t2.AlbumId """

        cursor.execute(query,)

        for row in cursor:
            if row["a1"] in idMap and row["a2"] in idMap:
                result.append( (idMap[row["a1"]], idMap[row["a2"]]) )

        cursor.close()
        conn.close()
        return result
