package com.grupo3.meetings.api.DTO;


import java.time.LocalDate;

public class EventDTO {

    private String nombreDeEvento;
    private String descripcion;
    private String ubicacion;

    private LocalDate fecha;

    private String hora;
    private String username;

    public EventDTO(String nombreDeEvento, String descripcion, String ubicacion, LocalDate fecha, String hora, String userAdmin) {
        this.nombreDeEvento = nombreDeEvento;
        this.descripcion = descripcion;
        this.ubicacion = ubicacion;
        this.fecha = fecha;
        this.hora = hora;
        this.username = userAdmin;
    }

    public EventDTO(String reunionDeDiscord) {
        this.nombreDeEvento = reunionDeDiscord;
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


    public LocalDate getFecha() {
        return fecha;
    }

    public void setFecha(LocalDate fecha) {
        this.fecha = fecha;
    }
}
