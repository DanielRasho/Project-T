import matplotlib;
import matplotlib.pyplot as pyplot;
import numpy as numpy;
import database_access as db;
import utils;
from database_enums import DatosUsuario, DatosBusqueda, ModoOrden;
from enum import Enum;

class TipoGrafica(Enum):
    BARRAS = 'barras';
    CIRCULAR = 'circular';

#PARÁMETROS = tipo: TipoGrafica Ej: TipoGrafica.BARRAS
#RETORNAR   = Nada
#MUESTRA LA GRÁFICA DE USUARIOS AGRUPADOS POR EDAD
def usuarios_por_edad(tipo: TipoGrafica):
    usuarios = db.agrupar_usuarios_por_columna(DatosUsuario.EDAD);
    eje_x = list(map(lambda x: x[0], usuarios));
    eje_y = list(map(lambda x: x[1], usuarios));
    
    if (tipo == TipoGrafica.CIRCULAR):
        labels = utils.agregar_label_lista(eje_x, 'años') 
        porcentajes = utils.porcentajes_de_valores(eje_y);        
        explode = utils.obtener_explode(porcentajes);
        
        fig, axs = pyplot.subplots()
        fig.canvas.manager.set_window_title('Estadísticas');
        
        axs.pie(porcentajes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90);
        axs.axis('equal');
        axs.set_title('Gráfica Edades');
        pyplot.legend();
    
    elif (tipo == TipoGrafica.BARRAS):
        fig, axs = pyplot.subplots();
        fig.canvas.manager.set_window_title('Estadísticas');
        
        axs.set_ylabel('Cantidad De Usuarios');
        axs.set_title('Gráfica Edades');
        
        eje_x = utils.agregar_label_lista(eje_x, 'años');
        axs.set_yticks(range(min(eje_y), max(eje_y) + 1));
        
        pyplot.bar(eje_x, eje_y);
    
    pyplot.show();     


#PARÁMETROS = tipo: TipoGrafica Ej: TipoGrafica.CIRCULAR
#RETORNAR   = Nada
#MUESTRA LA GRÁFICA DE USUARIOS AGRUPADOS POR GÉNERO
def usuarios_por_genero(tipo: TipoGrafica):
    usuarios = db.agrupar_usuarios_por_columna(DatosUsuario.GENERO);
    eje_x = list(map(lambda x: 'Masculino' if x[0] == 0 else 'Femenino', usuarios));
    eje_y = list(map(lambda x: x[1], usuarios));
    
    if (tipo == TipoGrafica.CIRCULAR):
        labels = eje_x;
        porcentajes = utils.porcentajes_de_valores(eje_y);
        explode = utils.obtener_explode(porcentajes);
        
        fig, axs = pyplot.subplots()
        fig.canvas.manager.set_window_title('Estadísticas');
        
        axs.pie(porcentajes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90);
        axs.axis('equal');
        axs.set_title('Genéro De Usuarios');
        pyplot.legend();
        
    elif (tipo == TipoGrafica.BARRAS):
        fig, axs = pyplot.subplots();
        fig.canvas.manager.set_window_title('Estadísticas');
        
        axs.set_xlabel('Genéro');
        axs.set_ylabel('Cantidad');
        axs.set_title('Genéro De Usuarios');
        
        axs.set_yticks(range(min(eje_y), max(eje_y) + 1));
        
        pyplot.bar(eje_x, eje_y);
        
    pyplot.show();
   
    
#PARÁMETROS = tipo: TipoGrafica Ej: TipoGrafica.CIRCULAR
#RETORNAR   = Nada
#MUESTRA LA GRÁFICA DE BÚSQUEDAS AGRUPADOS POR CONTEO
def busquedas_por_conteo(tipo: TipoGrafica):
    busquedas = db.obtener_busquedas();
    eje_x = list(map(lambda x: x[0], busquedas));
    eje_y = list(map(lambda x: x[1], busquedas));
    
    if (tipo == TipoGrafica.CIRCULAR):
        labels = eje_x;
        porcentajes = utils.porcentajes_de_valores(eje_y);
        explode = utils.obtener_explode(porcentajes);
        
        fig, axs = pyplot.subplots()
        fig.canvas.manager.set_window_title('Estadísticas');
        
        axs.pie(porcentajes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90);
        axs.axis('equal');
        axs.set_title('Gráfica Búsquedas');
        pyplot.legend();
        
    elif (tipo == TipoGrafica.BARRAS):
        fig, axs = pyplot.subplots();
        fig.canvas.manager.set_window_title('Estadísticas');
        
        axs.set_xlabel('Búsqueda');
        axs.set_ylabel('Veces Buscado');
        axs.set_title('Gráfica Búsquedas');
        
        axs.set_yticks(range(min(eje_y), max(eje_y) + 1));
        
        pyplot.bar(eje_x, eje_y);
        
    pyplot.show();