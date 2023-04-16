package com.grupo3.meetings.api.DTO;


public class EventDTO {

    private String nombreDeEvento;
    private String descripcion;
    private String ubicacion;

    private String fecha;

    private String hora;
    private String username;

    public EventDTO(String nombreDeEvento, String descripcion, String ubicacion, String fecha, String hora, String userAdmin) {
        this.nombreDeEvento = nombreDeEvento;
        this.descripcion = descripcion;
        this.ubicacion = ubicacion;
        this.fecha = fecha;
        this.hora = hora;
        this.username = userAdmin;
    }

    public String getNombreDeEvento() {
        return nombreDeEvento;
    }

    public void setNombreDeEvento(String nombreDeEvento) {
        this.nombreDeEvento = nombreDeEvento;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }

    public String getUbicacion() {
        return ubicacion;
    }

    public void setUbicacion(String ubicacion) {
        this.ubicacion = ubicacion;
    }

    public String getFecha() {
        return fecha;
    }

    public void setFecha(String fecha) {
        this.fecha = fecha;
    }

    public String getHora() {
        return hora;
    }

    public void setHora(String hora) {
        this.hora = hora;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }
}
