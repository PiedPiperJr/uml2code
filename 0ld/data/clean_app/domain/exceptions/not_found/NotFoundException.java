package org.enspy.4gi.domain.exceptions.not_found;

public class EntityNotFoundException extends RuntimeException {
    public EntityNotFoundException(String message) {
        super(message);
    }
}