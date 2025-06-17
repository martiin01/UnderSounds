from fastapi.templating import Jinja2Templates
from fastapi import Request
import json

# Configuramos Jinja2 para que las plantillas se encuentren en el directorio "view/"
templates = Jinja2Templates(directory="view/templates")

class View:
    def __init__(self):
        pass

    #NO_LOGEADO
    def getPrincipalNo_Log(self, request: Request, productos: dict):
        return templates.TemplateResponse("pag_principal_NoLog.html", {
            "request": request,
            "productos": productos
        })

    def getExplorarNo_Log(self, request: Request, productos: dict):
        return templates.TemplateResponse("pag_explorar_NoLog.html", {
            "request": request,
            "productos": productos
        })
        
    def getDetalleDiscoNo_Log(self, request: Request, disco: dict):
        return templates.TemplateResponse("descripcion_Disco_NoLog.html", {
            "request": request,
            "disco": disco
        })
        
    def getDetalleCamisetaNo_Log(self, request: Request, camiseta: dict):
        return templates.TemplateResponse("descripcion_Camiseta_NoLog.html", {
            "request": request,
            "camiseta": camiseta
        })

    def getCarritoNo_Log(self, request: Request, carrito: dict):
        return templates.TemplateResponse("carrito1_NoLog.html", {
            "request": request,
            "productos": carrito
        })
        
    def getPag_CamisetasNo_Log(self, request: Request, camisetas: dict):
        return templates.TemplateResponse("pag_camisetas_NoLog.html", {
            "request": request,
            "productos": camisetas
        })
        
    def getPag_CassettesNo_Log(self, request: Request, cassettes: dict):
        return templates.TemplateResponse("pag_cassettes_NoLog.html", {
            "request": request,
            "productos": cassettes
        })
        
    def getPag_CdsNo_Log(self, request: Request, cds: dict):
        return templates.TemplateResponse("pag_cds_NoLog.html", {
            "request": request,
            "productos": cds
        })
        
    def getPag_VinilosNo_Log(self, request: Request, vinilos: dict):
        return templates.TemplateResponse("pag_vinilos_NoLog.html", {
            "request": request,
            "productos": vinilos
        })
    
    def getPagoNo_Log(self, request: Request, pago: dict):
        return templates.TemplateResponse("pago_NoLog.html", {
            "request": request,
            "pago": pago
        })
        
    def getRegistroNo_Log(self, request: Request, registro: dict):
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "productos": registro
        })

#USUARIO
    def getPrincipalUsuario(self, request: Request, productos: dict):
        return templates.TemplateResponse("pag_principal_Usuario.html", {
            "request": request,
            "productos": productos
        })

    def getExplorarUsuario(self, request: Request, productos: dict):
        return templates.TemplateResponse("pag_explorar_Usuario.html", {
            "request": request,
            "productos": productos
        })
        
    def getDetalleDiscoUsuario(self, request: Request, disco: dict):
        return templates.TemplateResponse("descripcion_Disco_Usuario.html", {
            "request": request,
            "disco": disco
        })
        
    def getDetalleCamisetaUsuario(self, request: Request, camiseta: dict):
        return templates.TemplateResponse("descripcion_Camiseta_Usuario.html", {
            "request": request,
            "disco": camiseta
        })

    def getCarritoUsuario(self, request: Request, carrito: dict):
        return templates.TemplateResponse("carrito1_Usuario.html", {
            "request": request,
            "productos": carrito
        })
        
    def getPag_CamisetasUsuario(self, request: Request, camisetas: dict):
        return templates.TemplateResponse("pag_camisetas_Usuario.html", {
            "request": request,
            "productos": camisetas
        })
        
    def getPag_CassettesUsuario(self, request: Request, cassettes: dict):
        return templates.TemplateResponse("pag_cassettes_Usuario.html", {
            "request": request,
            "productos": cassettes
        })
        
    def getPag_CdsUsuario(self, request: Request, cds: dict):
        return templates.TemplateResponse("pag_cds_Usuario.html", {
            "request": request,
            "productos": cds
        })
        
    def getPag_VinilosUsuario(self, request: Request, vinilos: dict):
        return templates.TemplateResponse("pag_vinilos_Usuario.html", {
            "request": request,
            "productos": vinilos
        })
    
    def getPagoUsuario(self, request: Request, pago: dict):
        return templates.TemplateResponse("pago_Usuario.html", {
            "request": request,
            "pago": pago
        })
        
    def getRegistroUsuario(self, request: Request, registro: dict):
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "productos": registro
        })
        
    def getPerfilUsuario(self, request: Request, perfil_Usuario: dict):
        return templates.TemplateResponse("perfil_Usuario.html", {
            "request": request,
            "perfil": perfil_Usuario
        })
    
    def getComprasUsuario(self, request: Request, mis_compras: dict):
        return templates.TemplateResponse("mis_Compras_Usuario.html", {
            "request": request,
            "productos": mis_compras
        })
    
    def getLogInUsuario(self, request: Request, login: dict):
        return templates.TemplateResponse("loginLog.html", {
            "request": request,
            "productos": login
        })

#ARTISTA
    def getPrincipalArtista(self, request: Request, productos: dict):
        return templates.TemplateResponse("pag_principal_Artista.html", {
            "request": request,
            "productos": productos
        })

    def getExplorarArtista(self, request: Request, productos: dict):
        return templates.TemplateResponse("pag_explorar_Artista.html", {
            "request": request,
            "productos": productos
        })
        
    def getDetalleDiscoArtista(self, request: Request, disco: dict):
        return templates.TemplateResponse("descripcion_Disco_Artista.html", {
            "request": request,
            "disco": disco
        })
        
    def getDetalleCamisetaArtista(self, request: Request, camiseta: dict):
        return templates.TemplateResponse("descripcion_Camiseta_Artista.html", {
            "request": request,
            "disco": camiseta
        })

    def getCarritoArtista(self, request: Request, carrito: dict):
        return templates.TemplateResponse("carrito1_Artista.html", {
            "request": request,
            "productos": carrito
        })
        
    def getPag_CamisetasArtista(self, request: Request, camisetas: dict):
        return templates.TemplateResponse("pag_camisetas_Artista.html", {
            "request": request,
            "productos": camisetas
        })
        
    def getPag_CassettesArtista(self, request: Request, cassettes: dict):
        return templates.TemplateResponse("pag_cassettes_Artista.html", {
            "request": request,
            "productos": cassettes
        })
        
    def getPag_CdsArtista(self, request: Request, cds: dict):
        return templates.TemplateResponse("pag_cds_Artista.html", {
            "request": request,
            "productos": cds
        })
        
    def getPag_VinilosArtista(self, request: Request, vinilos: dict):
        return templates.TemplateResponse("pag_vinilos_Artista.html", {
            "request": request,
            "productos": vinilos
        })
    
    def getPagoArtista(self, request: Request, pago: dict):
        return templates.TemplateResponse("pago_Artista.html", {
            "request": request,
            "pago": pago
        })
        
    def getRegistroArtista(self, request: Request, registro: dict):
        return templates.TemplateResponse("registro_Artista.html", {
            "request": request,
            "productos": registro
        })
        
    def getPerfilArtista(self, request: Request, perfil_Artista: dict):
        return templates.TemplateResponse("perfil_Artista.html", {
            "request": request,
            "perfil": perfil_Artista
        })
    
    def getComprasArtista(self, request: Request, mis_compras: dict):
        return templates.TemplateResponse("mis_Compras_Artista.html", {
            "request": request,
            "productos": mis_compras
        })
    
    def getLogInArtista(self, request: Request, login: dict):
        return templates.TemplateResponse("loginArtista.html", {
            "request": request,
            "productos": login
        })
        
    def getForoArtista(self, request: Request, data: dict):
        return templates.TemplateResponse("foro_artistalog.html", {
            "request": request,
            "productos": data
        })
    
    def getMenuArtista(self, request: Request):
        return templates.TemplateResponse("menuPoductos_Artistas.html", {
            "request": request,
        })
    
    def getMerchandisingArtista(self, request: Request, products: dict):
        return templates.TemplateResponse("tus_merch.html", {
            "request": request,
            "productos": products
        })
        
    def getEstadisticas(self, request: Request, datos_est: dict):
        return templates.TemplateResponse("estadisticas.html", {
            "request": request,
            "productos": datos_est
        })
    
    def getProductosMusicales(self, request: Request, datos_prods: dict):
        return templates.TemplateResponse("prodMusicales.html", {
            "request": request,
            "productos": datos_prods
        })
    
    def getSubirProdMusicales(self, request: Request):
        return templates.TemplateResponse("subir_ProdMusicales.html", {
            "request": request,
        })
        
    def getSubirMerch(self, request: Request):
        return templates.TemplateResponse("subir_Merch.html", {
            "request": request,
        })

