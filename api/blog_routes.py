"""
Endpoints API para Blog/Noticias
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database.models import get_db, BlogPost
from datetime import datetime
import re

router = APIRouter()

def crear_slug(titulo):
    """Convertir título a slug URL-friendly"""
    slug = titulo.lower()
    slug = re.sub(r'[áàäâ]', 'a', slug)
    slug = re.sub(r'[éèëê]', 'e', slug)
    slug = re.sub(r'[íìïî]', 'i', slug)
    slug = re.sub(r'[óòöô]', 'o', slug)
    slug = re.sub(r'[úùüû]', 'u', slug)
    slug = re.sub(r'[ñ]', 'n', slug)
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug

@router.get("/blog", tags=["Blog - Público"])
def listar_posts_publico(
    categoria: str = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Obtener posts publicados (público)"""
    query = db.query(BlogPost).filter(BlogPost.publicado == True)
    
    if categoria:
        query = query.filter(BlogPost.categoria == categoria)
    
    total = query.count()
    posts = query.order_by(desc(BlogPost.fecha_publicacion)).offset(offset).limit(limit).all()
    
    return {
        "success": True,
        "total": total,
        "posts": [
            {
                "id": post.id,
                "titulo": post.titulo,
                "slug": post.slug,
                "extracto": post.extracto,
                "categoria": post.categoria,
                "autor_nombre": post.autor_nombre,
                "imagen_portada": post.imagen_portada,
                "visitas": post.visitas,
                "destacado": post.destacado,
                "fecha_publicacion": post.fecha_publicacion.isoformat() if post.fecha_publicacion else None
            }
            for post in posts
        ]
    }

@router.get("/blog/{slug}", tags=["Blog - Público"])
def obtener_post(slug: str, db: Session = Depends(get_db)):
    """Obtener post individual por slug"""
    post = db.query(BlogPost).filter(
        BlogPost.slug == slug,
        BlogPost.publicado == True
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    
    # Incrementar visitas
    post.visitas += 1
    db.commit()
    
    return {
        "success": True,
        "post": {
            "id": post.id,
            "titulo": post.titulo,
            "slug": post.slug,
            "contenido": post.contenido,
            "extracto": post.extracto,
            "categoria": post.categoria,
            "autor_nombre": post.autor_nombre,
            "imagen_portada": post.imagen_portada,
            "visitas": post.visitas,
            "meta_description": post.meta_description,
            "meta_keywords": post.meta_keywords,
            "fecha_publicacion": post.fecha_publicacion.isoformat() if post.fecha_publicacion else None,
            "created_at": post.created_at.isoformat(),
            "updated_at": post.updated_at.isoformat()
        }
    }

@router.get("/blog/categorias/listar", tags=["Blog - Público"])
def listar_categorias(db: Session = Depends(get_db)):
    """Obtener categorías disponibles con conteo"""
    categorias = db.query(
        BlogPost.categoria,
        db.func.count(BlogPost.id).label('total')
    ).filter(
        BlogPost.publicado == True
    ).group_by(BlogPost.categoria).all()
    
    return {
        "success": True,
        "categorias": [
            {"nombre": cat[0], "total_posts": cat[1]}
            for cat in categorias if cat[0]
        ]
    }

@router.get("/admin/blog", tags=["Admin - Blog"])
def listar_todos_posts_admin(
    categoria: str = None,
    publicado: bool = None,
    db: Session = Depends(get_db)
):
    """Listar todos los posts (admin)"""
    query = db.query(BlogPost)
    
    if categoria:
        query = query.filter(BlogPost.categoria == categoria)
    if publicado is not None:
        query = query.filter(BlogPost.publicado == publicado)
    
    posts = query.order_by(desc(BlogPost.created_at)).all()
    
    return {
        "success": True,
        "total": len(posts),
        "posts": [
            {
                "id": post.id,
                "titulo": post.titulo,
                "slug": post.slug,
                "categoria": post.categoria,
                "publicado": post.publicado,
                "destacado": post.destacado,
                "visitas": post.visitas,
                "fecha_publicacion": post.fecha_publicacion.isoformat() if post.fecha_publicacion else None,
                "created_at": post.created_at.isoformat()
            }
            for post in posts
        ]
    }

@router.post("/admin/blog", tags=["Admin - Blog"])
def crear_post(datos: dict, db: Session = Depends(get_db)):
    """Crear nuevo post"""
    try:
        slug = crear_slug(datos.get('titulo', ''))
        
        # Verificar slug único
        existe = db.query(BlogPost).filter(BlogPost.slug == slug).first()
        if existe:
            slug = f"{slug}-{int(datetime.now().timestamp())}"
        
        nuevo_post = BlogPost(
            titulo=datos.get('titulo'),
            slug=slug,
            contenido=datos.get('contenido'),
            extracto=datos.get('extracto', ''),
            categoria=datos.get('categoria', 'general'),
            autor_nombre=datos.get('autor_nombre', 'Equipo Editorial'),
            imagen_portada=datos.get('imagen_portada', ''),
            meta_description=datos.get('meta_description', ''),
            meta_keywords=datos.get('meta_keywords', ''),
            publicado=datos.get('publicado', False),
            destacado=datos.get('destacado', False),
            fecha_publicacion=datetime.now() if datos.get('publicado') else None
        )
        
        db.add(nuevo_post)
        db.commit()
        db.refresh(nuevo_post)
        
        return {
            "success": True,
            "message": "Post creado exitosamente",
            "post_id": nuevo_post.id,
            "slug": nuevo_post.slug
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/admin/blog/{post_id}", tags=["Admin - Blog"])
def actualizar_post(post_id: int, datos: dict, db: Session = Depends(get_db)):
    """Actualizar post existente"""
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    
    try:
        # Actualizar campos
        if 'titulo' in datos:
            post.titulo = datos['titulo']
            post.slug = crear_slug(datos['titulo'])
        if 'contenido' in datos:
            post.contenido = datos['contenido']
        if 'extracto' in datos:
            post.extracto = datos['extracto']
        if 'categoria' in datos:
            post.categoria = datos['categoria']
        if 'autor_nombre' in datos:
            post.autor_nombre = datos['autor_nombre']
        if 'imagen_portada' in datos:
            post.imagen_portada = datos['imagen_portada']
        if 'meta_description' in datos:
            post.meta_description = datos['meta_description']
        if 'meta_keywords' in datos:
            post.meta_keywords = datos['meta_keywords']
        if 'publicado' in datos:
            post.publicado = datos['publicado']
            if datos['publicado'] and not post.fecha_publicacion:
                post.fecha_publicacion = datetime.now()
        if 'destacado' in datos:
            post.destacado = datos['destacado']
        
        post.updated_at = datetime.now()
        db.commit()
        
        return {
            "success": True,
            "message": "Post actualizado exitosamente",
            "slug": post.slug
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/admin/blog/{post_id}", tags=["Admin - Blog"])
def eliminar_post(post_id: int, db: Session = Depends(get_db)):
    """Eliminar post"""
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    
    try:
        titulo = post.titulo
        db.delete(post)
        db.commit()
        
        return {
            "success": True,
            "message": f"Post '{titulo}' eliminado exitosamente"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
